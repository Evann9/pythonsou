let bpMap = null;
let bpMarkerSource = null;
let bpLineSource = null;
let bpPermitSource = null;
let bpPermitLayer = null;
let bpCoords = [];
let bpEditIndex = null;
let bpLastWeatherCoord = null;
let bpApprovedPermits = [];

const BP_DEFAULT_CENTER = [127.031794, 37.498799];

const BP_LIMITS = {
    maxWaypoints: 4,
    minWind: 0,
    maxWind: 5,
    minAltitude: 10,
    maxAltitude: 200,
    minDistance: 0,
    maxDistance: 1500,
    minRotation: 0,
    maxRotation: 720
};

function bpSetWindStatus(message, isError = false) {
    const status = document.getElementById('bp-wind-status');
    if (!status) return;

    status.textContent = message;
    status.classList.toggle('error', isError);
}

function bpSetWindValue(windValue, sourceCoord = null) {
    const windInput = document.getElementById('bp-wind');
    if (!windInput) return;

    const rawWind = Number(windValue);

    if (!Number.isFinite(rawWind)) {
        windInput.value = '';
        bpSetWindStatus('풍속 값을 확인할 수 없습니다.', true);
        return;
    }

    const limitedWind = Math.min(
        Math.max(rawWind, BP_LIMITS.minWind),
        BP_LIMITS.maxWind
    );

    windInput.value = limitedWind.toFixed(1);

    if (rawWind > BP_LIMITS.maxWind) {
        bpSetWindStatus(`기상청 풍속 ${rawWind.toFixed(1)}m/s → 모델 제한상 5.0m/s로 적용`, false);
    } else if (sourceCoord) {
        bpSetWindStatus(`기상청 풍속 ${limitedWind.toFixed(1)}m/s 자동 적용`, false);
    } else {
        bpSetWindStatus(`풍속 ${limitedWind.toFixed(1)}m/s 적용`, false);
    }
}

async function bpFetchWindByCoord(coord) {
    const windInput = document.getElementById('bp-wind');
    if (!windInput || !coord) return;

    bpLastWeatherCoord = coord;
    windInput.value = '';
    bpSetWindStatus('기상청 풍속 조회 중...');

    try {
        const response = await fetch(`/api/weather?lat=${coord.lat}&lon=${coord.lng}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || data.message || '날씨 조회 실패');
        }

        const wind = Number(data.wind);

        if (!Number.isFinite(wind)) {
            throw new Error('응답에 풍속 정보가 없습니다.');
        }

        bpSetWindValue(wind, coord);

    } catch (error) {
        console.error('배터리 예측용 풍속 조회 실패:', error);
        windInput.value = '';
        bpSetWindStatus('풍속 조회 실패: 기상청 API 키 또는 날씨 데이터 상태를 확인해주세요.', true);
    }
}

function bpRefreshWindFromLatestCoord() {
    if (bpCoords.length === 0) {
        const windInput = document.getElementById('bp-wind');
        if (windInput) windInput.value = '';
        bpSetWindStatus('좌표를 선택하면 기상청 API 기준 풍속이 자동 입력됩니다.');
        return;
    }

    const latestCoord = bpCoords[bpCoords.length - 1];
    bpFetchWindByCoord(latestCoord);
}

function bpMakePermitStyle(feature) {
    const kind = feature.get('kind');

    if (kind === 'permit-pin') {
        return new ol.style.Style({
            image: new ol.style.Circle({
                radius: 11,
                fill: new ol.style.Fill({ color: '#22c55e' }),
                stroke: new ol.style.Stroke({ color: '#ffffff', width: 3 })
            }),
            text: new ol.style.Text({
                text: '✓',
                font: 'bold 13px sans-serif',
                fill: new ol.style.Fill({ color: '#ffffff' })
            })
        });
    }

    return new ol.style.Style({
        fill: new ol.style.Fill({ color: 'rgba(34, 197, 94, 0.22)' }),
        stroke: new ol.style.Stroke({
            color: 'rgba(34, 197, 94, 0.95)',
            width: 2,
            lineDash: [6, 4]
        })
    });
}

function bpIsApprovedPermit(permitOrStatus) {
    if (!permitOrStatus) return false;

    if (typeof permitOrStatus === 'object') {
        const p = permitOrStatus;

        if (p.is_approved === true || p.approved === true) return true;

        const values = [
            p.status,
            p.state,
            p.approval_status,
            p.approvalStatus,
            p.result,
            p.status_text,
            p.statusText
        ];

        return values.some(value => bpIsApprovedPermit(value));
    }

    const text = String(permitOrStatus).trim().toLowerCase();

    return [
        '승인',
        'approved',
        'approve',
        'accepted',
        '허가',
        'permit',
        'permitted',
        '완료',
        'y',
        'yes',
        'true',
        '1'
    ].includes(text);
}

function bpGetPermitRadius(permit) {
    const radius = Number(permit.radius || permit.flight_radius || permit.permit_radius || 500);
    return Number.isFinite(radius) && radius > 0 ? radius : 500;
}

function bpCreatePermitCircleFeature(permit) {
    const lng = Number(permit.lng);
    const lat = Number(permit.lat);

    if (!Number.isFinite(lat) || !Number.isFinite(lng)) return null;

    const center = ol.proj.fromLonLat([lng, lat]);
    const pointResolution = ol.proj.getPointResolution('EPSG:3857', 1, center);
    const radius = bpGetPermitRadius(permit);

    const circle = new ol.geom.Circle(center, radius / pointResolution);
    const polygon = ol.geom.Polygon.fromCircle(circle, 96);

    const feature = new ol.Feature({ geometry: polygon });
    feature.set('kind', 'permit-area');
    feature.set('permit', permit);

    return feature;
}

function bpCreatePermitPinFeature(permit) {
    const lng = Number(permit.lng);
    const lat = Number(permit.lat);

    if (!Number.isFinite(lat) || !Number.isFinite(lng)) return null;

    const feature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([lng, lat]))
    });

    feature.set('kind', 'permit-pin');
    feature.set('permit', permit);

    return feature;
}

function bpIsProjectedCoordInsideApprovedPermit(projectedCoord) {
    if (!bpPermitSource) return false;

    const areaFeatures = bpPermitSource
        .getFeatures()
        .filter(feature => feature.get('kind') === 'permit-area');

    if (areaFeatures.length === 0) return false;

    return areaFeatures.some(feature => {
        const geometry = feature.getGeometry();
        if (!geometry) return false;

        if (typeof geometry.intersectsCoordinate === 'function') {
            return geometry.intersectsCoordinate(projectedCoord);
        }

        return false;
    });
}

function bpCenterMapOnFirstApprovedPermit() {
    if (!bpMap || !bpPermitSource || bpApprovedPermits.length === 0) return;

    const firstPermit = bpApprovedPermits[0];

    const areaFeature = bpPermitSource.getFeatures().find(feature => {
        return feature.get('kind') === 'permit-area' && feature.get('permit') === firstPermit;
    });

    const lng = Number(firstPermit.lng);
    const lat = Number(firstPermit.lat);

    if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

    if (areaFeature && areaFeature.getGeometry()) {
        bpMap.getView().fit(areaFeature.getGeometry().getExtent(), {
            padding: [70, 70, 70, 70],
            maxZoom: 16,
            duration: 300
        });
    } else {
        bpMap.getView().animate({
            center: ol.proj.fromLonLat([lng, lat]),
            zoom: 16,
            duration: 300
        });
    }
}


function bpNormalizePermit(rawPermit) {
    const p = { ...rawPermit };

    p.lat = p.lat ?? p.latitude ?? p.center_lat ?? p.centerLat ?? p.y;
    p.lng = p.lng ?? p.lon ?? p.longitude ?? p.center_lng ?? p.centerLng ?? p.x;
    p.radius = p.radius ?? p.flight_radius ?? p.permit_radius ?? p.range_m ?? p.range ?? 500;

    p.region = p.region ?? p.district ?? p.address ?? p.addr ?? p.area ?? p.location ?? p.region_name;
    p.purpose = p.purpose ?? p.reason ?? p.flight_purpose ?? p.title ?? p.name ?? p.area_name ?? p.zone_name;

    p.start_date = p.start_date ?? p.startDate ?? p.from_date ?? p.flight_start ?? p.period_start;
    p.end_date = p.end_date ?? p.endDate ?? p.to_date ?? p.flight_end ?? p.period_end;

    return p;
}

function bpGetPermitTimeValue(permit) {
    const candidates = [
        permit.created_at,
        permit.createdAt,
        permit.submitted_at,
        permit.submittedAt,
        permit.apply_date,
        permit.application_date,
        permit.requested_at,
        permit.updated_at,
        permit.id,
        permit.permit_id
    ];

    for (const value of candidates) {
        if (value === undefined || value === null || value === '') continue;

        if (typeof value === 'number') return value;

        const parsedDate = Date.parse(value);
        if (!Number.isNaN(parsedDate)) return parsedDate;

        const parsedNumber = Number(value);
        if (Number.isFinite(parsedNumber)) return parsedNumber;
    }

    return 0;
}

function bpSortPermitsByRecentFirst(permits) {
    return [...permits].sort((a, b) => bpGetPermitTimeValue(b) - bpGetPermitTimeValue(a));
}

function bpGetPermitLabel(permit, index) {
    const region =
        permit.region ||
        permit.district ||
        permit.address ||
        permit.location ||
        permit.area_name ||
        permit.zone_name ||
        '';

    const purpose =
        permit.purpose ||
        permit.reason ||
        permit.flight_purpose ||
        permit.title ||
        permit.name ||
        '';

    if (region && purpose) {
        return `${index + 1}. ${region} / ${purpose}`;
    }

    if (region) {
        return `${index + 1}. ${region}`;
    }

    if (purpose) {
        return `${index + 1}. ${purpose}`;
    }

    return `${index + 1}. 승인구역`;
}

function bpGetPermitStatusText(permit) {
    const status = permit.status || permit.state || permit.approval_status || permit.status_text || '승인';
    return String(status);
}

function bpFormatPermitPeriod(permit) {
    const start = permit.start_date || permit.startDate || permit.from_date || permit.flight_start || '';
    const end = permit.end_date || permit.endDate || permit.to_date || permit.flight_end || '';

    if (start && end) return `${start} ~ ${end}`;
    if (start) return String(start);
    if (end) return String(end);
    return '-';
}

function bpCenterMapOnPermit(permit) {
    if (!bpMap || !permit) return;

    const areaFeature = bpPermitSource
        ? bpPermitSource.getFeatures().find(feature => {
            return feature.get('kind') === 'permit-area' && feature.get('permit') === permit;
        })
        : null;

    const lng = Number(permit.lng);
    const lat = Number(permit.lat);

    if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

    if (areaFeature && areaFeature.getGeometry()) {
        bpMap.getView().fit(areaFeature.getGeometry().getExtent(), {
            padding: [70, 70, 70, 70],
            maxZoom: 16,
            duration: 300
        });
    } else {
        bpMap.getView().animate({
            center: ol.proj.fromLonLat([lng, lat]),
            zoom: 16,
            duration: 300
        });
    }
}

function bpCenterMapOnLatestApprovedPermit() {
    if (!bpApprovedPermits || bpApprovedPermits.length === 0) return;

    bpCenterMapOnPermit(bpApprovedPermits[0]);
}

function bpRenderPermitCardList() {
    const list = document.getElementById('bp-permit-card-list');
    const empty = document.getElementById('bp-permit-empty');
    if (!list || !empty) return;

    list.innerHTML = '';

    if (!bpApprovedPermits || bpApprovedPermits.length === 0) {
        empty.style.display = 'block';
        return;
    }

    empty.style.display = 'none';

    bpApprovedPermits.forEach((permit, index) => {
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'bp-permit-card';
        card.onclick = function() {
            bpCenterMapOnPermit(permit);
        };

        const period = bpFormatPermitPeriod(permit);
        const label = bpGetPermitLabel(permit, index);

        card.innerHTML = `
            <div class="bp-permit-card-top">
                <span class="bp-permit-status-dot"></span>
                <span class="bp-permit-status-text">${bpGetPermitStatusText(permit)}</span>
                <span class="bp-permit-card-no">#${index + 1}</span>
            </div>
            <div class="bp-permit-card-title">${label}</div>
            <div class="bp-permit-card-meta">기간 ${period}</div>
        `;

        list.appendChild(card);
    });
}

async function bpLoadUserApprovedPermits() {
    if (!bpMap || !bpPermitSource) return;

    try {
        const response = await fetch('/api/my_permits');
        const data = await response.json();

        bpPermitSource.clear();
        bpApprovedPermits = [];

        if (!data.ok || !data.permits || data.permits.length === 0) {
            console.log('배터리 예측 페이지: 표시할 내 허가 구역 없음');
            bpRenderPermitCardList();
            return;
        }

        const normalizedPermits = data.permits
            .map(bpNormalizePermit)
            .filter(p => Number.isFinite(Number(p.lat)) && Number.isFinite(Number(p.lng)));

        bpApprovedPermits = bpSortPermitsByRecentFirst(
            normalizedPermits.filter(p => bpIsApprovedPermit(p))
        );

        // 일부 API 응답에서 승인 상태 필드명이 다르게 내려오는 경우가 있어,
        // 승인 필터 결과가 0건이면 좌표가 있는 신청 건을 표시 대상으로 사용합니다.
        if (bpApprovedPermits.length === 0 && normalizedPermits.length > 0) {
            bpApprovedPermits = bpSortPermitsByRecentFirst(normalizedPermits);
        }

        bpApprovedPermits.forEach(p => {
            const areaFeature = bpCreatePermitCircleFeature(p);
            const pinFeature = bpCreatePermitPinFeature(p);

            if (areaFeature) bpPermitSource.addFeature(areaFeature);
            if (pinFeature) bpPermitSource.addFeature(pinFeature);
        });

        console.log(`배터리 예측 페이지: 내 승인 구역 ${bpApprovedPermits.length}건 표시`);
        bpRenderPermitCardList();
        bpCenterMapOnLatestApprovedPermit();

    } catch (error) {
        console.warn('배터리 예측 페이지 내 허가 구역 로드 실패:', error);
    }
}

function bpTryAddOrEditCoordFromMap(evt) {
    const projectedCoord = evt.coordinate;

    if (!bpIsProjectedCoordInsideApprovedPermit(projectedCoord)) {
        alert('승인된 비행 허가 구역 안에서만 좌표를 선택할 수 있습니다.');
        return;
    }

    const [lng, lat] = ol.proj.toLonLat(projectedCoord);

    const newCoord = {
        lat: Number(lat.toFixed(6)),
        lng: Number(lng.toFixed(6))
    };

    if (!bpIsManualCoordInsideApprovedPermit(newCoord)) {
        alert('승인된 비행 허가 구역 안의 좌표만 입력할 수 있습니다.');
        return;
    }

    if (bpEditIndex !== null) {
        bpCoords[bpEditIndex] = newCoord;
        bpEditIndex = null;
        bpRenderCoords();
        bpFetchWindByCoord(newCoord);
        return;
    }

    if (bpCoords.length >= BP_LIMITS.maxWaypoints) {
        alert('좌표는 최대 4개까지만 입력할 수 있습니다.');
        return;
    }

    bpCoords.push(newCoord);
    bpRenderCoords();
    bpFetchWindByCoord(newCoord);
}

function bpIsManualCoordInsideApprovedPermit(coord) {
    if (!bpMap || !coord) return false;

    const projected = ol.proj.fromLonLat([coord.lng, coord.lat]);
    return bpIsProjectedCoordInsideApprovedPermit(projected);
}

function bpInitMap() {
    if (bpMap) {
        setTimeout(() => bpMap.updateSize(), 100);
        bpLoadUserApprovedPermits();
        return;
    }

    const baseLayer = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: `http://api.vworld.kr/req/wmts/1.0.0/${VWORLD_KEY}/Base/{z}/{y}/{x}.png`,
            maxZoom: 19,
            crossOrigin: 'anonymous'
        })
    });

    bpPermitSource = new ol.source.Vector();

    bpPermitLayer = new ol.layer.Vector({
        source: bpPermitSource,
        style: bpMakePermitStyle,
        zIndex: 5
    });

    bpLineSource = new ol.source.Vector();

    const lineLayer = new ol.layer.Vector({
        source: bpLineSource,
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: '#2563eb',
                width: 3
            })
        }),
        zIndex: 10
    });

    bpMarkerSource = new ol.source.Vector();

    const markerLayer = new ol.layer.Vector({
        source: bpMarkerSource,
        style: function(feature) {
            const idx = feature.get('index');

            return new ol.style.Style({
                image: new ol.style.Circle({
                    radius: 6,
                    fill: new ol.style.Fill({ color: '#1e3a5f' }),
                    stroke: new ol.style.Stroke({ color: '#93c5fd', width: 2 })
                }),
                text: new ol.style.Text({
                    text: String(idx),
                    offsetY: -14,
                    font: '12px sans-serif',
                    fill: new ol.style.Fill({ color: '#0f172a' }),
                    backgroundFill: new ol.style.Fill({ color: 'rgba(255,255,255,0.8)' }),
                    padding: [2, 4, 2, 4]
                })
            });
        },
        zIndex: 20
    });

    bpMap = new ol.Map({
        target: 'battery-vmap',
        layers: [baseLayer, bpPermitLayer, lineLayer, markerLayer],
        view: new ol.View({
            center: ol.proj.fromLonLat(BP_DEFAULT_CENTER),
            zoom: 16,
            minZoom: 6,
            maxZoom: 19
        }),
        controls: new ol.Collection([])
    });

    bpMap.on('click', bpTryAddOrEditCoordFromMap);

    bpLoadUserApprovedPermits();
    setTimeout(() => bpMap.updateSize(), 150);
}

function bpAddManualCoord() {
    const lat = parseFloat(document.getElementById('bp-manual-lat').value.trim());
    const lng = parseFloat(document.getElementById('bp-manual-lng').value.trim());

    if (isNaN(lat) || isNaN(lng)) {
        alert('올바른 위도와 경도를 입력해주세요.');
        return;
    }

    const newCoord = {
        lat: Number(lat.toFixed(6)),
        lng: Number(lng.toFixed(6))
    };

    if (bpEditIndex !== null) {
        bpCoords[bpEditIndex] = newCoord;
        bpEditIndex = null;
    } else {
        if (bpCoords.length >= BP_LIMITS.maxWaypoints) {
            alert('좌표는 최대 4개까지만 입력할 수 있습니다.');
            return;
        }

        bpCoords.push(newCoord);
    }

    document.getElementById('bp-manual-lat').value = '';
    document.getElementById('bp-manual-lng').value = '';

    bpRenderCoords();
    bpFetchWindByCoord(newCoord);
}

function bpSelectCoordForEdit(index) {
    bpEditIndex = index;
    bpRenderCoords();

    const result = document.getElementById('bp-result');

    if (result) {
        result.innerHTML = `
            <div><strong>${index + 1}번 좌표 수정 모드</strong></div>
            <div>지도에서 허가 구역 안의 새 위치를 클릭하면 해당 좌표가 변경됩니다.</div>
            <div>또는 위도/경도를 수동 입력한 뒤 수동 좌표 추가 버튼을 눌러도 수정됩니다.</div>
        `;
    }
}

function bpCancelCoordEdit() {
    bpEditIndex = null;
    bpRenderCoords();
    bpUpdateDistanceDisplay();
}

function bpRemoveCoord(index) {
    bpCoords.splice(index, 1);
    bpEditIndex = null;
    bpRenderCoords();
    bpRefreshWindFromLatestCoord();
}

function bpMoveCoordUp(index) {
    if (index <= 0) return;

    const temp = bpCoords[index - 1];
    bpCoords[index - 1] = bpCoords[index];
    bpCoords[index] = temp;

    bpEditIndex = null;
    bpRenderCoords();
}

function bpMoveCoordDown(index) {
    if (index >= bpCoords.length - 1) return;

    const temp = bpCoords[index + 1];
    bpCoords[index + 1] = bpCoords[index];
    bpCoords[index] = temp;

    bpEditIndex = null;
    bpRenderCoords();
}

function bpRemoveLastCoord() {
    if (bpCoords.length === 0) return;

    bpCoords.pop();
    bpEditIndex = null;
    bpRenderCoords();
    bpRefreshWindFromLatestCoord();
}

function bpClearCoords() {
    bpCoords = [];
    bpEditIndex = null;

    bpRenderCoords();
    bpClearChart();

    const windInput = document.getElementById('bp-wind');
    if (windInput) windInput.value = '';
    bpSetWindStatus('좌표를 선택하면 기상청 API 기준 풍속이 자동 입력됩니다.');

    document.getElementById('bp-result').textContent =
        '좌표와 고도를 입력한 뒤 배터리 예측 버튼을 눌러주세요.';
}

function bpRenderCoords() {
    const list = document.getElementById('bp-coord-list');
    const empty = document.getElementById('bp-empty-message');

    list.innerHTML = '';
    empty.style.display = bpCoords.length ? 'none' : 'block';

    bpCoords.forEach((coord, index) => {
        const item = document.createElement('div');
        item.className = 'bp-coord-item';

        if (bpEditIndex === index) {
            item.classList.add('editing');
        }

        item.onclick = function() {
            bpSelectCoordForEdit(index);
        };

        item.innerHTML = `
            <div class="bp-coord-index">${index + 1}</div>

            <div class="bp-coord-text">
                위도 ${coord.lat.toFixed(6)} / 경도 ${coord.lng.toFixed(6)}
                ${bpEditIndex === index ? '<div class="bp-edit-hint">지도에서 허가 구역 안의 새 위치를 클릭하면 이 좌표가 수정됩니다.</div>' : ''}
            </div>

            <div style="display:flex; gap:6px;">
                <button type="button" class="bp-move-btn" onclick="event.stopPropagation(); bpMoveCoordUp(${index})">▲</button>
                <button type="button" class="bp-move-btn" onclick="event.stopPropagation(); bpMoveCoordDown(${index})">▼</button>
                <button type="button" class="bp-delete-btn" onclick="event.stopPropagation(); bpRemoveCoord(${index})">삭제</button>
            </div>
        `;

        list.appendChild(item);
    });

    bpRefreshMapFeatures();

    if (bpEditIndex === null) {
        bpUpdateDistanceDisplay();
    }
}

function bpRefreshMapFeatures() {
    if (!bpMap || !bpMarkerSource || !bpLineSource) return;

    bpMarkerSource.clear();
    bpLineSource.clear();

    if (bpCoords.length === 0) {
        return;
    }

    const projected = bpCoords.map((coord, idx) => {
        const point = ol.proj.fromLonLat([coord.lng, coord.lat]);
        const feature = new ol.Feature(new ol.geom.Point(point));

        feature.set('index', idx + 1);
        bpMarkerSource.addFeature(feature);

        return point;
    });

    if (projected.length >= 2) {
        const closedPath = [...projected, projected[0]];
        const lineFeature = new ol.Feature(new ol.geom.LineString(closedPath));
        bpLineSource.addFeature(lineFeature);
    }
}

function bpCalculateDistanceMeters(lat1, lng1, lat2, lng2) {
    const R = 6371000;
    const toRad = deg => deg * Math.PI / 180;

    const dLat = toRad(lat2 - lat1);
    const dLng = toRad(lng2 - lng1);

    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
        Math.sin(dLng / 2) * Math.sin(dLng / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
}

function bpGetTotalDistanceMeters() {
    if (bpCoords.length < 2) return 0;

    let total = 0;

    for (let i = 0; i < bpCoords.length - 1; i++) {
        total += bpCalculateDistanceMeters(
            bpCoords[i].lat,
            bpCoords[i].lng,
            bpCoords[i + 1].lat,
            bpCoords[i + 1].lng
        );
    }

    total += bpCalculateDistanceMeters(
        bpCoords[bpCoords.length - 1].lat,
        bpCoords[bpCoords.length - 1].lng,
        bpCoords[0].lat,
        bpCoords[0].lng
    );

    return total;
}

function bpGetBearingDegrees(lat1, lng1, lat2, lng2) {
    const toRad = deg => deg * Math.PI / 180;
    const toDeg = rad => rad * 180 / Math.PI;

    const phi1 = toRad(lat1);
    const phi2 = toRad(lat2);
    const dLng = toRad(lng2 - lng1);

    const y = Math.sin(dLng) * Math.cos(phi2);
    const x =
        Math.cos(phi1) * Math.sin(phi2) -
        Math.sin(phi1) * Math.cos(phi2) * Math.cos(dLng);

    return (toDeg(Math.atan2(y, x)) + 360) % 360;
}

function bpAngleDiffDegrees(a, b) {
    let diff = Math.abs(a - b) % 360;
    return diff > 180 ? 360 - diff : diff;
}

function bpGetTotalRotationDegrees() {
    if (bpCoords.length < 2) return 0;

    const closed = [...bpCoords, bpCoords[0]];
    const bearings = [];

    for (let i = 0; i < closed.length - 1; i++) {
        bearings.push(
            bpGetBearingDegrees(
                closed[i].lat,
                closed[i].lng,
                closed[i + 1].lat,
                closed[i + 1].lng
            )
        );
    }

    let totalRotation = 0;

    for (let i = 0; i < bearings.length; i++) {
        const current = bearings[i];
        const next = bearings[(i + 1) % bearings.length];
        totalRotation += bpAngleDiffDegrees(current, next);
    }

    return Math.min(Math.max(totalRotation, 0), 720);
}

function bpGetModelDistanceMeters(altitude) {
    if (bpCoords.length === 1) {
        return altitude;
    }

    return bpGetTotalDistanceMeters();
}

function bpGetModelRotationDegrees() {
    if (bpCoords.length === 1) {
        return 0;
    }

    return bpGetTotalRotationDegrees();
}

function bpFormatDistance(distance) {
    if (distance >= 1000) {
        return `${distance.toFixed(1)} m (${(distance / 1000).toFixed(3)} km)`;
    }

    return `${distance.toFixed(1)} m`;
}

function bpUpdateDistanceDisplay() {
    const result = document.getElementById('bp-result');
    if (!result) return;

    if (bpCoords.length === 0) {
        result.innerHTML = `
            <div>입력 좌표 수: <strong>0개</strong> / 최대 4개</div>
            <div>비행 거리: <strong>좌표를 1개 이상 입력하면 계산됩니다.</strong></div>
            <div>좌표 제한: <strong>승인된 비행 허가 구역 안에서만 선택 가능</strong></div>
        `;
        return;
    }

    if (bpCoords.length === 1) {
        const altitudeValue = parseFloat(document.getElementById('bp-altitude').value.trim());

        if (isNaN(altitudeValue)) {
            result.innerHTML = `
                <div>입력 좌표 수: <strong>1개</strong> / 최대 4개</div>
                <div>비행 방식: <strong>단일 좌표 수직 비행</strong></div>
                <div>비행 거리: <strong>고도 입력 후 계산됩니다.</strong></div>
                <div>총회전량: <strong>0 deg</strong></div>
            `;
            return;
        }

        result.innerHTML = `
            <div>입력 좌표 수: <strong>1개</strong> / 최대 4개</div>
            <div>비행 방식: <strong>단일 좌표 수직 비행</strong></div>
            <div>현재 비행 거리: <strong>${altitudeValue.toFixed(1)} m</strong></div>
            <div>총회전량: <strong>0 deg</strong></div>
            <div>비행 경로: <strong>이륙 후 입력 고도까지 상승 기준</strong></div>
        `;
        return;
    }

    const totalDistance = bpGetTotalDistanceMeters();
    const totalRotation = bpGetTotalRotationDegrees();

    result.innerHTML = `
        <div>입력 좌표 수: <strong>${bpCoords.length}개</strong> / 최대 4개</div>
        <div>현재 비행 거리: <strong>${bpFormatDistance(totalDistance)}</strong></div>
        <div>총회전량: <strong>${totalRotation.toFixed(1)} deg</strong></div>
        <div>비행 경로: <strong>마지막 지점에서 1번 좌표로 복귀 포함</strong></div>
    `;
}

function bpValidateInputs() {
    const altitude = parseFloat(document.getElementById('bp-altitude').value.trim());
    const wind = parseFloat(document.getElementById('bp-wind').value.trim());

    if (isNaN(altitude)) {
        alert('비행 고도를 입력해주세요.');
        return null;
    }

    if (altitude < BP_LIMITS.minAltitude || altitude > BP_LIMITS.maxAltitude) {
        alert('비행 고도는 10~200m 범위로 입력해야 합니다.');
        return null;
    }

    if (isNaN(wind)) {
        alert('풍속 정보가 없습니다. 좌표를 선택해 기상청 풍속을 먼저 조회해주세요.');
        return null;
    }

    if (wind < BP_LIMITS.minWind || wind > BP_LIMITS.maxWind) {
        alert('풍속은 0~5m/s 범위로 입력해야 합니다.');
        return null;
    }

    if (bpCoords.length < 1) {
        alert('좌표를 최소 1개 이상 입력해주세요.');
        return null;
    }

    if (bpCoords.length > BP_LIMITS.maxWaypoints) {
        alert('좌표는 최대 4개까지만 입력할 수 있습니다.');
        return null;
    }

    const distance = bpGetModelDistanceMeters(altitude);
    const rotation = bpGetModelRotationDegrees();

    if (distance <= BP_LIMITS.minDistance) {
        alert('비행 거리는 0보다 커야 합니다.');
        return null;
    }

    if (distance > BP_LIMITS.maxDistance) {
        alert('비행 거리는 최대 1500m 이하로 입력해야 합니다.');
        return null;
    }

    if (rotation < BP_LIMITS.minRotation || rotation > BP_LIMITS.maxRotation) {
        alert('총회전량은 0~720deg 범위여야 합니다.');
        return null;
    }

    return {
        altitude,
        wind,
        distance,
        rotation
    };
}

async function bpPredictBattery() {
    const inputs = bpValidateInputs();
    const result = document.getElementById('bp-result');

    if (!inputs) return;

    bpEditIndex = null;
    bpRenderCoords();

    result.innerHTML = '배터리 예측 모델 계산 중입니다...';

    try {
        const response = await fetch('/api/battery/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(inputs)
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            alert(data.message || '배터리 예측 중 오류가 발생했습니다.');
            bpUpdateDistanceDisplay();
            return;
        }

        const routeText = bpCoords.length === 1
            ? '단일 좌표 수직 비행 / 회전량 없음'
            : '마지막 지점에서 1번 좌표로 복귀';

        result.innerHTML = `
            <div>풍속: <strong>${inputs.wind.toFixed(1)} m/s</strong></div>
            <div>입력 고도: <strong>${inputs.altitude.toFixed(0)} m</strong></div>
            <div>입력 좌표 수: <strong>${bpCoords.length}개</strong></div>
            <div>비행 거리: <strong>${bpFormatDistance(inputs.distance)}</strong></div>
            <div>총회전량: <strong>${inputs.rotation.toFixed(1)} deg</strong></div>
            <div>비행 경로: <strong>${routeText}</strong></div>
            <div>예상 배터리 소모율: <strong>${data.result.predicted_consumption}%</strong></div>
            <div>예상 잔여 배터리: <strong>${data.result.predicted_remaining}%</strong></div>
        `;

        bpDrawBatteryChart(data.graph.distance, data.graph.battery);

    } catch (error) {
        console.error(error);
        alert('서버와 통신 중 오류가 발생했습니다.');
        bpUpdateDistanceDisplay();
    }
}

function bpDrawBatteryChart(distanceValues, batteryValues) {
    const canvas = document.getElementById('bp-battery-chart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    const paddingLeft = 52;
    const paddingRight = 20;
    const paddingTop = 24;
    const paddingBottom = 42;

    const chartW = width - paddingLeft - paddingRight;
    const chartH = height - paddingTop - paddingBottom;

    const maxX = Math.max(...distanceValues);
    const minX = 0;
    const minY = 0;
    const maxY = 100;

    function xScale(x) {
        return paddingLeft + ((x - minX) / (maxX - minX)) * chartW;
    }

    function yScale(y) {
        return paddingTop + ((maxY - y) / (maxY - minY)) * chartH;
    }

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, width, height);

    bpDrawBatteryBand(ctx, paddingLeft, paddingTop, chartW, chartH, yScale, 25, 30, '#facc15', 'WARNING');
    bpDrawBatteryBand(ctx, paddingLeft, paddingTop, chartW, chartH, yScale, 15, 20, '#fb923c', 'RTL');
    bpDrawBatteryBand(ctx, paddingLeft, paddingTop, chartW, chartH, yScale, 5, 10, '#ef4444', 'CRITICAL');

    ctx.strokeStyle = '#cbd5e1';
    ctx.lineWidth = 1;

    ctx.beginPath();
    ctx.moveTo(paddingLeft, paddingTop);
    ctx.lineTo(paddingLeft, paddingTop + chartH);
    ctx.lineTo(paddingLeft + chartW, paddingTop + chartH);
    ctx.stroke();

    ctx.fillStyle = '#64748b';
    ctx.font = '12px sans-serif';

    for (let y = 0; y <= 100; y += 20) {
        const py = yScale(y);

        ctx.fillText(String(y), 18, py + 4);

        ctx.strokeStyle = '#e2e8f0';
        ctx.beginPath();
        ctx.moveTo(paddingLeft, py);
        ctx.lineTo(paddingLeft + chartW, py);
        ctx.stroke();
    }

    for (let i = 0; i <= 4; i++) {
        const xVal = minX + (maxX - minX) * (i / 4);
        const px = xScale(xVal);
        ctx.fillText(xVal.toFixed(0), px - 8, height - 16);
    }

    ctx.strokeStyle = '#16a34a';
    ctx.lineWidth = 3;
    ctx.beginPath();

    distanceValues.forEach((x, i) => {
        const px = xScale(x);
        const py = yScale(batteryValues[i]);

        if (i === 0) {
            ctx.moveTo(px, py);
        } else {
            ctx.lineTo(px, py);
        }
    });

    ctx.stroke();

    ctx.fillStyle = '#16a34a';

    distanceValues.forEach((x, i) => {
        const px = xScale(x);
        const py = yScale(batteryValues[i]);

        ctx.beginPath();
        ctx.arc(px, py, 4, 0, Math.PI * 2);
        ctx.fill();
    });

    ctx.fillStyle = '#0f172a';
    ctx.font = '13px sans-serif';
    ctx.fillText('Distance (m)', width / 2 - 32, height - 4);

    ctx.save();
    ctx.translate(12, height / 2 + 36);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText('Battery (%)', 0, 0);
    ctx.restore();
}

function bpDrawBatteryBand(ctx, left, top, chartW, chartH, yScale, yMin, yMax, color, label) {
    const y1 = yScale(yMax);
    const y2 = yScale(yMin);

    ctx.fillStyle = color + '22';
    ctx.fillRect(left, y1, chartW, y2 - y1);

    ctx.fillStyle = color;
    ctx.font = 'bold 12px sans-serif';
    ctx.fillText(label, left + 8, y1 + 16);
}

function bpClearChart() {
    const canvas = document.getElementById('bp-battery-chart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

# 예외처리 : 파일, 네트워크, DB작업, 실행에러 등의 에러 대처
# 쓸까말까 고민되면 써라 (권장)

def divide(a,b):
    return a / b
print('이런 저런 작업 진행...')
# c = divide(5,2)
# c = divide(5,0)
# print(c)

try:
    # 실행문(예외 발생 가능 구문)
    c = divide(5,2)           # ZeroDivisionError
    # c = divide(5,0)
    print(c)

    aa = [1,2]                #  IndexError
    print(aa[0])
    print(aa[3])

    open("c:/work/abc.txt")

except ZeroDivisionError:   # 예외 종류 관련 클래스
    print('두번째 값은 0을 주면 안돼요')  # 예외 발생 처리 구문

except IndexError as err:
    print('참고범위 오류: ', err)

except Exception as e:
    print('에러: ', e)
    
finally:
    print('에러 유무에 상관없이 반드시 수행됨')


print('end')
print('종료')

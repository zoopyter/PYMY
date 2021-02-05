# Project Coding Convention


## [PEP8](https://www.python.org/dev/peps/pep-0008/) 기반
> 귀도의 중요한 통찰 중 하나는 프로그램 코드가 작성되는 횟수보다는 사람 에게 읽히는 횟수가 더 많다는 사실이다  
> 파이썬의 계명에는 “어떤 일을 하는 확실한 방법이 (될 수 있으면 하나만) 있어야한다” 라는 말이 있음
- PEP는 파이썬 개선 제안서이며 PEP8은 그중 8번째 문서로 파이썬 코드를 어떻게 구성할 지 알려주는 스타일 가이드 문서
    - 공통된 코딩 컨벤션을 유지한다면 개발 협업을 효율적으로 진행 가능
    - 가독성 높아짐
    - 유지보수가 쉬워짐
- 그중 기본젹인 내용을 3가지 항목으로 나누어 프로젝트의 코딩 컨벤션으로 이용

### (1)공백
- 한줄의 문자 길이가 79자 이하(VSCode의 Ruler 기능 이용)
- 함수와 클래스는 빈 줄 두개로 구분한다
```
def func1():
    pass
# 한줄
# 두줄
class ObjA():
    pass
```
- 클래스에서 메서드는 빈 줄 하나로 구분한다
```
class ObjA():
    def __init__(self):
        pass
    # 한줄
    def method1(self):
        pass
```
- 변수 할당시 = 앞뒤로 하나의 공백만 사용
```
# a(공백)=(공백)10
a = 10
```
- 리스트 인덱스, 함수 호출, 키워드 인수 할당에는 공백을 추가하지 않는다
```
a[0:10] # a는 리스트, 리스트 인덱싱시 : 양 옆에 no space
foo = bar(foo=bar) # 키워드 인수 할당, 함수호출
```
- 소괄호, 중괄호, 대괄호 사이에 추가로 공백을 넣지 않는다.


### (2) 명명규칙

- 모듈 이름은 되도록 짧아야하며, 모두 소문자로만 구성되어야 한다. 가독성을 향상시킬 수 있을 경우 언더스코어 사용 가능 
- 패키지의 이름 또한 짧으며 모두 소문자여야 하고 언더스코어는 사용 할 수 없다.
- 함수, 변수, 속성은 lowercase_underscore
- 클래스의 Protected 속성은 하나의 언더스코어를 이름 앞에 추가 _(변수명)능
- 클래스의 Private 속성은 두개의 언더스코어를 이름 앞에 추가 __(변수명)
- Class와 Exception은  첫글자 포함 각 단어의 맨앞글자만 대문자로 한다(파스칼 표기법) ex) TestClass
- 모듈수준 상수는 모두 대문자로 구성한다. ex) ALL_TYPE
- 클래스 내 인스턴스 메소드에서는 첫번째 파라미터의 이름을 self로 지정한다.
- 클래스 메소드의 첫번째 파라미터의 이름은 cls로 지정한다.
- 단일 글자 변수로 l(소문자 엘), I(대문자 아이), O(대문자 오)를 사용하지 않는다.

### (3) 표현식과 문장

- if not a is b 보다는 if a is not b 사용
- 길이를 확인할 때 == 사용 안함, 빈 값은 암시적으로 False가 된다고 가정
    ex) if len(list) == 0 대신 if not somelist
- 빈 값은 암시적으로 False로 가정
- 값이 있거나 할당된 객채는 암시적으로 True로 가정
- 한 줄로 된 if, for, while, except등의 복합문을 지양
- 파일 최상단에 import 수행
- import로 모듈 로드시 하나의 import에 하나의 모듈만 로드
- import는 표준라이브러리 모듈 > 서드파티 모듈 > 본인이 작성한 모듈 / 알파벳순
- 모듈을 임포트할 때는 모듈의 절대경로 사용!(절대 경로를 사용 하기 위해서는 engine 모듈을 설치 해야 함)
- 상대적인 임포트를 해야 한다면 명시적인 구문 사용 from . import foo(패키지와 모듈)


# Pylint

- 작성된 코드는 Pylint, flake8 같은 툴을 Linter로 사용하여 검사하거나, Black 같은 툴을 Formatter로 사용할 수 있음. 
Vscode 에서 Pylint를 사용하게 되면(설치 pip install pylint) Panel 창의 Problems 창에서 에러 메시지를 확인할 수 있다. 


* Pylint 설정과 예외 처리는 다음과 같다.
```
"python.linting.pylintEnabled": true,
"python.linting.enabled": true
"python.linting.lintOnSave": true,
"python.linting.pylintArgs":["
--disable = W0614"]

# Disabled messages
#    Pointless
#       W0142 = *args and **kwargs support
#       W0403 = Relative imports
#       W0613 = Unused argument
#       W0232 = Class has no __init__ method
#       R0903 = Too few public methods
#       R0913 = Too many arguments
#       C0103 = Invalid name
#       R0914 = Too many local variables
#       C0304 = Final newline missing
#
#    PyLint's module importation is unreliable
#       F0401 = Unable to import module
#       W0402 = Uses of a deprecated module
#       E1101 = Module x has no y member
#
#    Already an error when wildcard imports are used
#       W0614 = Unused import from wildcard
#
#    Stricter messages that can be disabled until everything else has been fixed
#       C0111 = Missing docstring
#       C0301 = Line too long
```
# Header and  Doc String
- header는 old 스타일이기는 하지만 필요에 따라 작성 할 수 있음
- 
```
=============================================================
# Created By  : Jeromie Kirchoff, add human
# Created Date: 2021-02-04
"""The Module Has Been Build for..."""
=============================================================
```

```
class CustomClass:
"""
클래스의 문서화 내용을 입력합니다.    
"""

    def custom_function(param):
        '''
        함수의 문서화 내용을 입력합니다.
        '''
        ... 코드  ...  

```
-------------------------
-참고 사이트   
https://kongdols-room.tistory.com/18
https://codechacha.com/ko/pythonic-and-pep8/
https://kenial.tistory.com/902
https://stackoverflow.com/questions/52123470/how-do-i-disable-pylint-unused-import-error-messages-in-vs-code
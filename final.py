import re
#числа
#строки
#арифм. операторы
pattern = re.compile(
    r"\s*(?:(\d+(?:\.\d+)?)|"
    r"([A-Za-z_]\w*)|"
    r"([()+*/|,-]))")
#разбтие на разные токены
def token_virajenie(string):
    tokens = []
    pos = 0
    while pos < len(string):
        #находим похожие на наш pattern выражения
        virajenie = pattern.match(string, pos)
        #на ошибки
        if not virajenie:
            #если только из табуляции
            if string[pos:].isspace():
                break
            raise ValueError(f"Неправильный символ: {string[pos]}")

        number, min_poisk, oper = virajenie.groups()

        if number is not None:
            tokens.append(number)
            
        elif min_poisk is not None:
            tokens.append(min_poisk)
            
        else:
            tokens.append(oper)
        #для того, чтобы перейти на следующий символ
        pos = virajenie.end()

    return tokens
#+-
def plus_and_minus(tokens, pos):
    result, pos = umnoj_and_delen(tokens, pos)

    while pos < len(tokens) and tokens[pos] in ("+", "-"):
        op = tokens[pos]
        right, pos = umnoj_and_delen(tokens, pos + 1)

        if op == "+":
            result = result + right
        else:
            result = result - right

    return result, pos
#*/
def umnoj_and_delen(tokens, pos):
    result, pos = unarn_minus(tokens, pos)

    while pos < len(tokens) and tokens[pos] in ("*", "/"):
        op = tokens[pos]
        right, pos = unarn_minus(tokens, pos+1)

        if op == "*":
            result = result*right
        else:
            if right == 0:
                raise ValueError("На ноль делить нельзя")
            result = result/right

    return result, pos
#unar-
def unarn_minus(tokens, pos):
    if pos >= len(tokens):
        raise ValueError("Ожидалось число")

    if tokens[pos] == "-":
        result, pos = unarn_minus(tokens, pos+1)
        return -1 * result, pos

    if tokens[pos] == "+":
        return unarn_minus(tokens, pos+1)

    return vse_dle_vichisleni(tokens, pos)
#смотрим число, выражение в скобках и оператор min
def vse_dle_vichisleni(tokens, pos):
    if pos >= len(tokens):
        raise ValueError("Что-то непонятное вконце")
    token = tokens[pos]
    #число
    if re.fullmatch(r"\d+(\.\d+)?", token):
        if "." in token:
            return float(token), pos+1
        
        return int(token), pos+1
    #скобки
    if token == "(":
        # Сразу проверяем, пусты ли скобки
        if pos + 1 < len(tokens) and tokens[pos+1] == ")":
            raise ValueError("Пустые скобки (): внутри нужно выражение")
        # запускаем все проверки занаво внутри скобок
        result, pos = pobitovoe_ili(tokens, pos+1)
        if pos >= len(tokens) or tokens[pos] != ")":
            raise ValueError("Не хватает закрывающей скобки ')'")
        
        return result, pos+1
    #min()
    if token == "min":
        if pos+1 >= len(tokens) or tokens[pos+1]!="(":
            raise ValueError("После min должна идти скобка '('")
        
        pos += 2  #после min и скобки
        #пустой вызов min()
        if pos >= len(tokens) or tokens[pos] == ")":
            raise ValueError("Нужен хотябы 1 аргумент в функции min")

        #аргумент не может начинаться с запятой
        if tokens[pos] == ",":
            raise ValueError("Перед первым аргументом min стоит запятая")

        arguments = []

        while True:
            #пустые аргументы
            if pos >= len(tokens) or tokens[pos] in (",", ")"):
                raise ValueError("Ожидался аргумент функции min")

            result, pos = pobitovoe_ili(tokens, pos)
            arguments.append(result)

            #проверка на )
            if pos >= len(tokens):
                raise ValueError("Не хватает закрывающей скобки ')' в min")

            if tokens[pos] == ")":
                return min(arguments), pos+1

            if tokens[pos] != ",":
                raise ValueError("Ожидалась запятая или ')' в функции min")

            #пропуск запятой
            pos += 1
            #аргумент после зпт
            if pos >= len(tokens) or tokens[pos] in (",", ")"):
                raise ValueError( "После запятой в min нужен аргумент")

    #доп проверки на min
    if token == ")":
        raise ValueError("Лишняя закрывающая скобка ')'")

    if token == ",":
        raise ValueError("Неожиданная запятая")

    raise ValueError(f"Ожидалось число, скобка или функция, получено: {token}")
# |
def pobitovoe_ili(tokens, pos):
    leftresult, pos = plus_and_minus(tokens, pos)

    while pos < len(tokens) and tokens[pos] == "|":
        right, pos = plus_and_minus(tokens, pos+1)

        if type(leftresult) is not int or type(right) is not int:
            raise ValueError("Оператор | требует целые числа")
        
        leftresult = leftresult | right
    return leftresult, pos
# сам calculator
def calculator(string):
    tokens = token_virajenie(string)

    if not tokens:
        raise ValueError("Выражение пустое")

    result, pos = pobitovoe_ili(tokens, 0)

    if pos != len(tokens):
        raise ValueError(f"Лишний токен: {tokens[pos]}")
    
    return result
#начало работы
while True:
    string = input("(Для выхода напишите Esc)| Выражение: ")
    if string.strip() == "Esc":
        break
    try:
        print(calculator(string))
    except ValueError as error:
        print("Ошибка:", error)



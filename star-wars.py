'''Вам нужно написать программу, которая загадывает персонажей “Звёздных войн”.
Загадав персонажа, программа показывает подсказку в виде частотного биграммного словосочетания из реплик этого персонажа,
и ждёт ответа пользователя, после чего сообщает, угадал он или нет.

Например, если загадан персонаж «THREEPIO», можно показать подсказку «Master Luke».
Реплики персонажей нужно брать из сценариев ЗВ, ссылка на страницу датасета сценариев.

Пользователь может попросить подсказку. Тогда нужно выдать в ответ какую-то (если есть) информацию
о загаданном персонаже из датасета2 ссылка на страницу датасета базы знаний ЗВ.

В задании обязательно использовать словарь. Когда читаете csv, используйте DictReader.

Пользователь может выбрать подмножество персонажей, одного из которых загадает программа
– нужно спросить список интересных персонажей в начале работы программы. '''

import random, csv, re

def script_reading():
    with open ('starwars4.txt', encoding='utf-8') as f:
        script = f.read()
    return script

def make_list_of_characters(script): #взяла не из датасета, а из скрипта, чтобы не было несоответствий
    parts = script.split('"')
    list_of_characters = []
    for part in parts:
        if part.isupper():
            if part not in list_of_characters:
                list_of_characters.append(part)
    return list_of_characters

def subset():
    print('Если хотите, введите интересных вам персонажей')
    my_subset = []
    while input() != '':
        my_subset.append(input())
    return my_subset

def riddle(list_of_characters, my_subset):
    if my_subset == []:
        return random.choice(list_of_characters)
    else:
        return random.choice(my_subset)

def make_prompt_bigram(character, script):
    freq = {}
    lines = script.splitlines()
    for line in lines:
        if ('"' + character) in line: #чтобы не было путаницы MAN, WOMAN, COMMANDER итд, добавили кавычку
            text = line.split('" "')[2]
            text = text.replace(',', '').replace('.', '').replace('!', '').replace('?', '')
            text = text.lower()
            text = text.split()
            for i in range(1, len(text)):
                bigram = text[i-1] + ' ' + text[i]
                if bigram not in freq:
                    freq[bigram] = 1
                else:
                    freq[bigram] += 1
    max_freq = 0
    prompt = ''
    for elem in freq:
        if freq[elem] > max_freq:
            max_freq = freq[elem]
            prompt = elem
    print('Подсказка: ', prompt)

def guess1(character):
    print('Попробуй угадай. Если нужна подсказка, только скажи...')
    var = input()
    while var != 'подсказка':
        if var == character:
            print('Ура! Правильно!')
            game = 'end'
            break
        else:
            print('Давай ещё раз. Или может быть подсказочку...')
            var = input()
    game = 'continue'
    return game

def dataset_reading():
    dataset = csv.DictReader(open('swcharacters.csv'))
    return dataset

def find_prompt_info(character, dataset):
    info = {}
    for row in dataset:
        if character.lower() in row['name'].lower():
            info = row
            del info['name']
            for key in info:
                if info[key] == 'NA':
                    del info[key]
    if info == {}:
        print('Сорян, в базе подсказочек ничего нет, угадывай как хочешь.')  
    return info

def make_prompt_info(info):
    prompt = random.choice(list(info.items()))
    prompt = prompt[0] + ': ' + prompt[1]
    print(prompt)

def guess2(character, info):
    print('Ну а теперь чё? Ничё?')
    game = ''
    var = input()
    while game != 'end':
        if var == character:
            print('Ура! Правильно!')
            game = 'end'
        elif var == 'подсказка':
            if info == {}:
                print('Ха. Мим. Ничего не будет. Угадывай дальше')
                var = input()
            else:
                print('Так уж и быть. Подсказка: ')
                make_prompt_info(info)
                var = input()
        else:
            print('Давай ещё раз. Или может быть подсказочку...')
            var = input()   

def main():
    script = script_reading() #читаем файл сценария
    list_of_characters = make_list_of_characters(script) #из файла сценария составляем список персонажей
    my_subset = subset() #пользователь может задать список интересных ему персонажей
    riddle_character = riddle(list_of_characters, my_subset) #из подмножества или всего множества выбираем случайного персонажа
    make_prompt_bigram(riddle_character, script) #подсказка 1 - самая частотная биграмма
    game = guess1(riddle_character) #процесс угадывания после 1 подсказки и переход на 2 подсказку
    if game == 'continue':
        dataset = dataset_reading()
        info = find_prompt_info(riddle_character, dataset)
        make_prompt_info(info)
        guess2(riddle_character, info) #примечание: угадывает, только если написать имя персонажа, как в сценарии. по-моему и так большая программа, чтобы все варианты учитывать

if __name__ == '__main__':
    main()
    
    
    

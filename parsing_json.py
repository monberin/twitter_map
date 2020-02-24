import json 

with open('file_to_parse.json', 'r', encoding='utf-8') as f:
    js = json.load(f)


def parsing(json_obj: dict):
    start_json = json_obj
    while isinstance(json_obj,(list,dict)):
        try:
            if isinstance(json_obj,dict):
                print('; '.join(json_obj.keys()))
                key = input('choose a key: ')
                json_obj = json_obj[key]
            if isinstance(json_obj,list):
                if len(json_obj) > 1:
                    print('there are {} values in this list.'.format(len(json_obj)))
                    ind = int(input('Which one to look into? '))
                    json_obj = json_obj[ind-1]
                elif len(json_obj) == 1:
                    json_obj = json_obj[0]
                else:
                    json_obj = ''
        except (IndexError, KeyError, ValueError):
            print('something went wrong, there is no key like that. Try again: ')
            json_obj = start_json
            continue
    if json_obj is None:
        print('info missing')
    else:
        print(json_obj)

parsing(js)
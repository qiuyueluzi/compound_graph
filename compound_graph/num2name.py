import json

roman_to_str = {"I": "Math_Logic", "II": "Sets_and_Topology", "III": "Algebra", "IV": "Number_Theory", "V": "Groups_and_Rep",
                "VI": "Alg_Geometry", "VII": "Geometry", "VIII": "Diff_Geometry", "IX": "Topology", "X": "Analysis",
                "XI": "Complex_An", "XII": "Func_An", "XIII": "Diff_Eqns", "XIV": "Spec_Func", "XV": "Num_An",
                "XVI": "Appl_An", "XVII": "Prob_Theory", "XVIII": "Stats", "XIX": "Disc_Math", 
                "XX": "Info_Math", "XXI": "Opt_Theory", "XXII": "Mech_Phys", "XXIII": "Hist_Math"}

def split_roman_and_num(s):
    # ローマ数字とアラビア数字の対応表を辞書型で作る
    roman_dict = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    # ローマ数字とアラビア数字の部分を空文字列に初期化する
    roman_part = ''
    num_part = ''
    # 新しい文字列の各文字についてループする
    for c in s:
        # 文字がローマ数字であれば、ローマ数字の部分に追加する
        if c in roman_dict:
            roman_part += c
        # 文字がアラビア数字であれば、アラビア数字の部分に追加する
        elif c.isdigit():
            num_part += c
        # 文字がどちらでもなければ、エラーを返す
        else:
            return 'Error: invalid character'
    # ローマ数字とアラビア数字の部分をタプルとして返す
    if num_part == '':
        return 'Error: nothing number'    
    return (roman_part, num_part)

def replace_number_to_name():
    if len(parent) >= 2:
        romanAndNum = parent[1] # "/I9/A"のI9の部分
        result = split_roman_and_num(romanAndNum)
        if result != 'Error: invalid character':
            roman, num = result
            if roman in roman_to_str:
                parent[1] = roman_to_str[roman] + num
                obj["data"]["parent"] = "/".join(parent)
            else:
                print('Invalid input: the Roman numeral does not exist')
        else:
            print(result)
    else:
        print('Invalid input: the string does not have enough elements')

graph_json = open('graph_attrs/graph_classHierar_test.json', 'r')
graph_objects = json.load(graph_json)



for obj in graph_objects["eleObjs"]:
    if obj["group"] == "nodes":
        id_slash = obj["data"]["id"]
        name = obj["data"]["name"]
        if obj["data"].get("parent"):
            parent_slash = obj["data"]["parent"]
            parent = parent_slash.split("/")
            if len(parent) >= 2:
                romanAndNum = parent[1] # "/I9/A"のI9の部分
                result = split_roman_and_num(romanAndNum)
                if result != 'Error: invalid character':
                    roman, num = result
                    if roman in roman_to_str:
                        parent[1] = roman_to_str[roman] + num
                        obj["data"]["parent"] = "/".join(parent)
                    else:
                        print('Invalid input: the Roman numeral does not exist')
                else:
                    print(result)
            else:
                print('Invalid input: the string does not have enough elements')

        id = id_slash.split("/")
        if len(id) >= 2:
            romanAndNum = id[1] # "/I9/A"のI9の部分
            result = split_roman_and_num(romanAndNum)
            if result != 'Error: invalid character':
                roman, num = result
                if roman in roman_to_str:
                    id[1] = roman_to_str[roman] + num
                    obj["data"]["id"] = "/".join(id)
                else:
                    print('Invalid input: the Roman numeral does not exist')
            else:
                print(result)
        else:
            print('Invalid input: the string does not have enough elements')

        if len(name) >= 2:
            romanAndNum = name # "/I9/A"のI9の部分
            result = split_roman_and_num(romanAndNum)
            if result != 'Error: invalid character':
                roman, num = result
                if roman in roman_to_str:
                    name = roman_to_str[roman] + num
                    obj["data"]["name"] = name
                else:
                    print('Invalid input: the Roman numeral does not exist')
            else:
                print(result)
        else:
            print('Invalid input: the string does not have enough elements')

for obj in graph_objects["parents"]:
    if obj["group"] == "nodes":
        id_slash = obj["data"]["id"]
        name = obj["data"]["name"]
        if obj["data"].get("parent"):
            parent_slash = obj["data"]["parent"]
            parent = parent_slash.split("/")
            if len(parent) >= 2:
                romanAndNum = parent[1] # "/I9/A"のI9の部分
                result = split_roman_and_num(romanAndNum)
                if result != 'Error: invalid character':
                    roman, num = result
                    if roman in roman_to_str:
                        parent[1] = roman_to_str[roman] + num
                        obj["data"]["parent"] = "/".join(parent)
                    else:
                        print('Invalid input: the Roman numeral does not exist')
                else:
                    print(result)
            else:
                print('Invalid input: the string does not have enough elements')

        id = id_slash.split("/")
        if len(id) >= 2:
            romanAndNum = id[1] # "/I9/A"のI9の部分
            result = split_roman_and_num(romanAndNum)
            if result != 'Error: invalid character':
                roman, num = result
                if roman in roman_to_str:
                    id[1] = roman_to_str[roman] + num
                    obj["data"]["id"] = "/".join(id)
                else:
                    print('Invalid input: the Roman numeral does not exist')
            else:
                print(result)
        else:
            print('Invalid input: the string does not have enough elements')

        if len(name) >= 2:
            romanAndNum = name # "/I9/A"のI9の部分
            result = split_roman_and_num(romanAndNum)
            if result != 'Error: invalid character':
                roman, num = result
                if roman in roman_to_str:
                    name = roman_to_str[roman] + num
                    obj["data"]["name"] = name
                else:
                    print('Invalid input: the Roman numeral does not exist')
            else:
                print(result)
        else:
            print('Invalid input: the string does not have enough elements')
        

with open('graph_attrs/graph_Hierar_replace.json', 'w') as f :
    json.dump(graph_objects, f, indent=4)

print(graph_objects)
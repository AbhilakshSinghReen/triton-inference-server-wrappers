from copy import deepcopy


def ordered_dedupe(input_list):
    seen = set()
    seen_add = seen.add
    return [x for x in input_list if not (x in seen or seen_add(x))]


def reversed_ordered_dedupe(input_list):
    reversed_input_list = deepcopy(input_list)
    reversed_input_list.reverse()
    
    reversed_deduped_input_list = ordered_dedupe(reversed_input_list)
    
    deduped_input_list = reversed_deduped_input_list
    deduped_input_list.reverse()
    return deduped_input_list


def list_of_dicts_find(input_list, target_key, target_value):
    for item in input_list:
        if item[target_key] == target_value:
            return item
    
    return None


def dict_values_gte(dict_1, dict_2):
    for key in dict_1.keys():
        if dict_1[key] < dict_2[key]:
            return False
    
    return True


def validate_occupied_resoruces(occupied_resources):
    for resource_name in occupied_resources.keys():
        if occupied_resources[resource_name] < 0.0 or occupied_resources[resource_name] > 1.0:
            print("validate_occupied_resoruces ---X FAIL")
            print(occupied_resources)
            raise ValueError(f"occupied_resources.{resource_name} is {occupied_resources[resource_name]}")

    return True
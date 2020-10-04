import os

def parse_ir_to_dict(ir_model_rd):
    ir_model_rd = ir_model_rd.replace("{","")
    ir_model_rd = ir_model_rd.replace("'","")
    ir_model_rd = ir_model_rd.replace(" ","")
    ir_model_rd = ir_model_rd.split("},")
    ir_model_rd = [item.replace("}","") for item in ir_model_rd]    
    ir_model_rd = [item.split(":") for item in ir_model_rd]
    ir_model_rd = [[y.split(",") for y in x] for x in ir_model_rd]    
    #print(ir_model_rd)
    btn_dict = {}
    for item in ir_model_rd:
#         print(item[0][0])
#         print(item[1][0])
        btn_dict[item[0][0]] = {item[1][0], item[1][1]}
    return btn_dict
    
def find_key(btn_dict, value):
    index=0
    for x in btn_dict.values():
        for y in x:
            if y == value: return list(btn_dict.keys())[index]
        index+=1

def main():
    model="fd"               
    filepath = "ir_code_"+str(model)+".txt"
    if os.path.exists(filepath):
        f = open(filepath, "r")
        ir_model_rd = f.read()
        #print(ir_model_rd)
        btn_dict = parse_ir_to_dict(ir_model_rd)
        #print(btn_dict)
        print(find_key(btn_dict, "1"))
        print(find_key(btn_dict, "0xfd00ff"))
        print(find_key(btn_dict, "00000000111111010000000011111111"))
        print(btn_dict["1"])
        f.close()
    else: print("IR code dictionary file not found. Turn on logging to create it.")

if __name__ == "__main__":
    main()
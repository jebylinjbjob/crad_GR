if __name__ == "__main__":
    print_str =""
    test_str_list = []
    with open("card.txt", "r") as file:
        for line in file:
            test_str_list.append(line.strip())
    
    count = 0
    for test_str in test_str_list:
        output_str = F"###########第{count}筆##############\n"
        output_str += F"test_str: {test_str}\ncard_CardCode: {test_str[0:6]}\ncard_date: {test_str[6:14]}\ncard_Time: {test_str[14:]}\n"
        print_str += output_str
        count += 1
       
    print(print_str)
    print(f"count: {count}")

    
    

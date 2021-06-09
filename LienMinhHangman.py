from random import randint
import json

def displayWelcome(data_list):
    asciiArt = """
    
  _      _              __  __ _       _       _    _                                         
 | |    (_)            |  \/  (_)     | |     | |  | |                                        
 | |     _  ___ _ __   | \  / |_ _ __ | |__   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 | |    | |/ _ \ '_ \  | |\/| | | '_ \| '_ \  |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |____| |  __/ | | | | |  | | | | | | | | | | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |______|_|\___|_| |_| |_|  |_|_|_| |_|_| |_| |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                                                                   __/ |                      
                                                                  |___/                       
"""
    print(asciiArt)
    print("\n--- Chào mừng đến với Liên Minh Hangman! ---")
    print(f"\nHiện tại đang có {len(data_list)} tướng ở phiên bản 11.11\n")
    print("Nhiệm vụ của bạn là phải đoán tên tướng dựa vào 1 kĩ năng của tướng đó")
    print('Bạn có thể gõ "/ff" để đầu hàng và xem câu trả lời')
    
    
def get_data(file_object):
    try:
        with open(file_object, 'r') as file:
            content = json.load(file)
            return content
    except:
        print("Lỗi đọc file. Kiểm tra xem bạn có file 'lienminh.json' ở cùng thư mục này chưa")
    finally:
        file.close()
        
    
def game_loop(data_list, score):
    lives = 5
    random_champ = data_list[randint(0, len(data_list) - 1)]
    # random_champ = data_list[len(data_list) - 5] # zed only hehe xd
    champName = random_champ["name"]
    abilities_list = random_champ["abilities"]
    ability_index = randint(0, len(abilities_list) - 1)
    random_ability = abilities_list[ability_index]
    spells = ['chiêu Q', 'chiêu W', 'chiêu E', 'chiêu R', 'nội tại']
    
    game_state = 'play'
    
    word_list = []
    guess_list = []
    trial_list = []
    for char in champName:
        word_list.append(char.lower())
        guess_list.append("")
    
    # Display player UI
    print(f'\nTên kĩ năng: "{random_ability}"\n{len(champName)} chữ cái')
    print('Mạng:', '♥️ ' * lives)
    print("\n" + " _ " * len(guess_list) + "\n\n")
    
    guess = input("Đoán xem: ")
    
    while True:
        # print(chr(27) + "[2J") # clear the terminal

        if guess == '/ff':
            score -= 1
            game_state = 'end'
        
        # This /help feature is still bugged
        # if guess == '/help':
        #     lives -= 1
        #     rand_index = randint(0, len(word_list) - 1)
        #     guess_list[rand_index] = word_list[rand_index]
        
        if game_state == 'play':
            
            if guess == "":
                print("Hãy nhập vào gì đó")
                guess = input("Đoán lại xem: ").lower()
            elif len(guess) > 1:
                print("Chỉ được nhập 1 lần 1 chữ thôii")
                guess = input("Đoán lại xem: ").lower()
            elif guess.isalpha() == False:
                print("Sai ký tự rồi")
                guess = input("Đoán lại xem: ").lower()
            elif guess in trial_list:
                print(f'Bạn đoán chữ {guess} rồi')
                guess = input("Đoán lại xem: ").lower()
                
            trial_list.append(guess)
            found = False
            foundCount = 0
            
            for i in range(len(champName)):
                if guess == word_list[i]:
                    guess_list[i] = guess
                    found = True
                    foundCount += 1
                    
            if found == True:
                print(f"Chữ {guess}, có {foundCount} chữ {guess}!\n")
            elif found == False:
                lives -= 1
                responses = ['Hổng có', 'Ko thấy', 'Đoán sai rồi', 'Không có', 'Gà', 'Hông có', 'Hông thấy']
                print(responses[randint(0,len(responses)-1)] + "\n")
                
            # Update player UI
            print(f'Tên kĩ năng: "{random_ability}"\n{len(champName)} chữ cái')
            print('Mạng:', '♥️ ' * lives + '\n')
            for i in range(len(guess_list)):
                if guess_list[i] == "":
                    print(" _ ", end="")
                else:
                    print(" " + guess_list[i], end=" ")
            print("\n\n")
            
            if lives == 0:
                score -= 1
                responses = ["Toang hẳn :'(", 'Còn cái nịt!', 'Feed ít thôi', 'Report..', 'Con gà']
                print(responses[randint(0,len(responses)-1)] + "\n")
                game_state = 'end'
            elif word_list == guess_list:
                score += 1
                responses = ["Được của ló :))", 'Ghêêêêê!', 'Uầy!', '15p gg nuôn', 'Được!', 'Hay!', 'Dữ!', 'Nai xừ!', 'Tiếp!']
                print(responses[randint(0,len(responses)-1)] + "\n")
                game_state = 'end'
            else:
                guess = input("Đoán xem: ").lower()
            
        elif game_state == 'end':
            print(f'"{random_ability}" là {spells[ability_index]} của {champName}.')
            print(f'Bạn đang có {score} điểm')
            repeat = input("\nEnter để game mới, 'gg' để nghỉ: ")
            if repeat.lower() == 'y' or repeat == '':
                random_champ = data_list[randint(0, len(data_list) - 1)]
                game_loop(data_list, score)
            elif repeat.lower() == 'gg':
                print("GGWP!\n")
                exit()
            else:
                print('Nhập sai rồi')
                repeat = input("\nEnter để game mới, 'gg' để nghỉ: ")
    
    
def main():
    file_obj = 'lienminh.json'
    data_list = get_data(file_obj)    
    score = 0
    displayWelcome(data_list)
    game_loop(data_list, score)


if __name__ == "__main__":
    main()
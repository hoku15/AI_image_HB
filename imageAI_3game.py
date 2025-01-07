import random
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

def setup_pipeline():
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

# 画像生成--------------------
def generate_image(pipe, prompt, output_path="output.png"):
    image = pipe(prompt).images[0]
    image.save(output_path)
    return output_path

# ワードリスト--------------------
def get_random_words():
    word_list = [
        "猫", "犬", "火山", "川", "森", "ロボット", "宇宙船", "ビーチ",
        "城", "鳥", "花", "夕日", "車", "ギター", "本", "ケーキ", "街", "星",
        "海", "パソコン", "ゲーム", "魚", "人"  
    ]
    return random.sample(word_list, 3)

# メインゲーム--------------------
def main():
    def start_game():
        start_frame.pack_forget()
        root.geometry("1000x800")
        loading_frame.pack(fill=tk.BOTH, expand=True)
        root.update()

        # 準備--------------------
        print("画像を生成中... しばらくお待ちください。")
        pipeline = setup_pipeline()

        # 単語ランダム選択--------------------
        global selected_words, attempts
        selected_words = get_random_words()
        print(f"生成ワード: {', '.join(selected_words)}")

        # プロンプト作成--------------------
        prompt = f"A scene containing {selected_words[0]}, {selected_words[1]}, and {selected_words[2]}."

        # 画像生成--------------------
        print("画像を生成中")
        image_path = generate_image(pipeline, prompt)
        print(f"ファイル名: {image_path}")

        # 画面の移行--------------------
        loading_frame.pack_forget()
        game_frame.pack(fill=tk.BOTH, expand=True)

        # 画像表示--------------------
        img = Image.open(image_path)
        img = img.resize((600, 400))
        tk_img = ImageTk.PhotoImage(img)
        img_label.config(image=tk_img)
        img_label.image = tk_img

    def check_guess():
        global attempts
        guesses = [guess_entry1.get().strip(), guess_entry2.get().strip(), guess_entry3.get().strip()]

        if any(not g for g in guesses):
            feedback_label.config(text="3つのワードを入力", fg="red")
            return

        # ヒット＆ブロー--------------------
        hit = sum([1 for i, g in enumerate(guesses) if g == selected_words[i]])
        blow = sum([1 for g in guesses if g in selected_words]) - hit

        feedback_label.config(text=f"{hit} ヒット！ {blow} ブロー！", fg="green")

        attempts -= 1
        attempts_label.config(text=f"残り試行回数: {attempts}")

        # 単語残し--------------------
        guess_entry1.delete(0, tk.END)
        guess_entry2.delete(0, tk.END)
        guess_entry3.delete(0, tk.END)
        guess_entry1.insert(0, guesses[0])
        guess_entry2.insert(0, guesses[1])
        guess_entry3.insert(0, guesses[2])

        if hit == 3:
            messagebox.showinfo("結果", "Congratulations!!!\n3ヒット！")
            retry_game()
        elif attempts == 0:
            messagebox.showinfo("結果", f"GAME OVER\n正解は: {', '.join(selected_words)}")
            retry_game()

    def retry_game():
        game_frame.pack_forget()
        root.geometry("600x400")  # スタート画面用のサイズに変更
        start_frame.pack(fill=tk.BOTH, expand=True)

    # GUIのセットアップ--------------------
    root = tk.Tk()
    root.title("AI画像ヒット＆ブロー")
    root.geometry("600x400")  # スタート画面用の初期サイズ
    root.resizable(False, False)  # ウィンドウサイズ変更を無効化

    # スタート画面--------------------
    start_frame = tk.Frame(root)
    start_frame.pack(fill=tk.BOTH, expand=True)

    start_label = tk.Label(start_frame, text="AI画像ヒット＆ブロー", font=("Arial", 24))
    start_label.pack(pady=50)

    start_button = tk.Button(start_frame, text="ゲームを開始", font=("Arial", 18), command=start_game)
    start_button.pack(pady=20)

    # ロード画面--------------------
    loading_frame = tk.Frame(root)
    loading_label = tk.Label(loading_frame, text="画像を生成中です... お待ちください。", font=("Arial", 20))
    loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # ゲーム画面--------------------
    game_frame = tk.Frame(root)

    img_label = tk.Label(game_frame)
    img_label.pack(pady=20)

    instruction_label = tk.Label(game_frame, text="画像を見て、3つの単語をそれぞれ入力してください。", font=("Arial", 18))
    instruction_label.pack(pady=10)

    input_frame = tk.Frame(game_frame)
    input_frame.pack(pady=20)

    tk.Label(input_frame, text="1", font=("Arial", 16)).grid(row=0, column=0, padx=5)
    guess_entry1 = tk.Entry(input_frame, font=("Arial", 16), width=15)
    guess_entry1.grid(row=0, column=1, padx=15)

    tk.Label(input_frame, text="2", font=("Arial", 16)).grid(row=0, column=2, padx=5)
    guess_entry2 = tk.Entry(input_frame, font=("Arial", 16), width=15)
    guess_entry2.grid(row=0, column=3, padx=15)

    tk.Label(input_frame, text="3", font=("Arial", 16)).grid(row=0, column=4, padx=5)
    guess_entry3 = tk.Entry(input_frame, font=("Arial", 16), width=15)
    guess_entry3.grid(row=0, column=5, padx=15)

    submit_button = tk.Button(game_frame, text="回答", font=("Arial", 18), command=check_guess)
    submit_button.pack(pady=20)

    feedback_label = tk.Label(game_frame, text="", font=("Arial", 18))
    feedback_label.pack(pady=10)

    attempts_label = tk.Label(game_frame, text="残り試行回数: 10", font=("Arial", 18))
    attempts_label.pack(pady=10)

    # 初期化--------------------
    global attempts
    attempts = 10

    root.mainloop()

if __name__ == "__main__":
    main()

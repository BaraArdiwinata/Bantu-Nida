import random
import time

class ChemistryGame:
    # BUG FIX: '__init__' harus menggunakan double underscore
    def __init__(self):  
        self.compounds = {
            "H2O": {
                "name": "air",
                "sifat": "Cairan tidak berwarna, pelarut universal"
            },
            "CO2": {
                "name": "karbon dioksida",
                "sifat": "Gas tidak berwarna, digunakan dalam minuman berkarbonasi"
            },
            "NaCl": {
                "name": "natrium klorida",
                "sifat": "Kristal putih, dikenal sebagai garam dapur"
            },
            "H2SO4": {
                "name": "asam sulfat",
                "sifat": "Cairan kental, sangat korosif"
            },
            "HCl": {
                "name": "asam klorida",
                "sifat": "Cairan asam kuat, digunakan dalam pembersih"
            },
            "NH3": {
                "name": "amonia",
                "sifat": "Gas dengan bau menyengat, digunakan dalam pupuk"
            },
            "CH4": {
                "name": "metana",
                "sifat": "Gas tidak berwarna, bahan bakar utama gas alam"
            },
            "C2H6": {
                "name": "etana",
                "sifat": "Gas tidak berwarna, digunakan dalam produksi etilena"
            },
            "C6H12O6": {
                "name": "glukosa",
                "sifat": "Kristal putih, sumber energi utama tubuh"
            },
            "CaCO3": {
                "name": "kalsium karbonat",
                "sifat": "Padatan putih, bahan utama kapur dan marmer"
            },
        }
        
        self.score = 0
        self.total_questions = 0
        
    def display_welcome(self):
        print("=" * 50)
        print("🧪 SELAMAT DATANG DI GAME IDENTIFIKASI SENYAWA KIMIA 🧪")
        print("=" * 50)
        print("Cara bermain:")
        print("1. Anda akan diberi rumus kimia")
        print("2. Tebak nama senyawa tersebut")
        print("3. Ketik 'quit' untuk keluar")
        print("4. Ketik 'hint' untuk mendapat petunjuk")
        print("=" * 50)
        print()
        
    def get_random_compound(self):
        formula = random.choice(list(self.compounds.keys()))
        name = self.compounds[formula]["name"]
        sifat = self.compounds[formula]["sifat"]
        return formula, name, sifat
        
    def give_hint(self, sifat):
        return sifat
        
    def check_answer(self, user_answer, correct_answer):
        user_answer = user_answer.lower().strip()
        correct_answer = correct_answer.lower().strip()
        
        return user_answer == correct_answer
        
    def play_round(self):
        formula, correct_name, sifat = self.get_random_compound()
        
        print(f"Rumus kimia: {formula}")
        print("Apa nama senyawa ini?")
        
        while True:
            user_input = input("Jawaban Anda: ").strip()
            
            if user_input.lower() == 'quit':
                return False
                
            if user_input.lower() == 'hint':
                hint = self.give_hint(sifat)
                print(f"Petunjuk: {hint}")
                continue
                
            if self.check_answer(user_input, correct_name):
                print("✅ Benar! Selamat!")
                self.score += 1
                break
            else:
                print(f"❌ Salah! Jawaban yang benar adalah: {correct_name}")
                break
        
        self.total_questions += 1
        print(f"Skor Anda: {self.score}/{self.total_questions}")
        print("-" * 30)
        return True
        
    def show_final_score(self):
        print("\n" + "=" * 50)
        print("🎯 HASIL AKHIR")
        print("=" * 50)
        print(f"Total pertanyaan: {self.total_questions}")
        print(f"Jawaban benar: {self.score}")
        print(f"Jawaban salah: {self.total_questions - self.score}")
        
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            print(f"Persentase: {percentage:.1f}%")
            
            if percentage >= 80:
                print("🏆 Luar biasa! Anda ahli kimia!")
            elif percentage >= 60:
                print("👍 Bagus! Terus belajar!")
            elif percentage >= 40:
                print("📚 Lumayan, masih perlu belajar lagi")
            else:
                print("💪 Jangan menyerah, terus belajar!")
        
        print("=" * 50)
        
    def start_game(self):
        self.display_welcome()
        
        while True:
            if not self.play_round():
                break # Keluar dari loop utama jika play_round return False (user ketik 'quit')
            
            # Loop untuk validasi input lanjut atau tidak
            while True:
                continue_game = input("\nIngin lanjut? (y/n): ").lower().strip()
                if continue_game in ['y', 'yes', 'ya']:
                    print()
                    break # Lanjut ke ronde berikutnya
                elif continue_game in ['n', 'no', 'tidak']:
                    self.show_final_score()
                    return # Keluar dari fungsi start_game
                else:
                    print("Masukkan 'y' untuk ya atau 'n' untuk tidak")
        
        # SUGGESTION: Baris ini bisa dihapus karena sudah di-handle di atas
        # Tapi jika user keluar dengan 'quit', baris ini akan menampilkan skor akhir
        self.show_final_score()

def main():
    game = ChemistryGame()
    game.start_game()
    print("\nTerima kasih sudah bermain! 🧪")

# BUG FIX: '__name__' dan '__main__' harus menggunakan double underscore
if __name__ == "__main__":
    main()
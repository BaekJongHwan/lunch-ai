import google.generativeai as genai
import PIL.Image
import os

# 1. Google AI Studio에서 받은 새 API 키를 입력하세요
genai.configure(api_key="AIzaSyC4fiZRe4KB6mTbhrmwN5d4DKw2DiQZ8D8")

def run_extraction():
    # 2. 모델 설정 (가장 최신이자 안정적인 이름)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    image_path = "menu.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ '{image_path}' 파일이 폴더에 없습니다!")
        return

    try:
        img = PIL.Image.open(image_path)
        print("🚀 분석을 시작합니다...")
        
        # 3. 분석 요청
        response = model.generate_content([
            "이 식단표 이미지에서 식당 이름과 메뉴를 JSON 형식으로 추출해줘.", 
            img
        ])
        
        print("\n✨ [드디어 성공!] 결과:")
        print(response.text)
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")

if __name__ == "__main__":
    run_extraction()
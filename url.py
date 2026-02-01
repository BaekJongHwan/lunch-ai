import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. 브라우저 설정
chrome_options = Options()
# 작동 확인을 위해 브라우저 창을 띄운 상태로 실행합니다.
# chrome_options.add_argument("--headless") 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # 2. 네이버 지도 식당 소식 탭 접속
    target_url = "https://map.naver.com/p/entry/place/1671594903?c=15.00,0,0,0,dh&placePath=/feed"
    driver.get(target_url)
    
    # 3. iframe 진입 대기 (필수 단계)
    wait = WebDriverWait(driver, 20)
    entry_iframe = wait.until(EC.presence_of_element_located((By.ID, "entryIframe")))
    driver.switch_to.frame(entry_iframe)
    print("✅ iframe 진입 성공")

    # 4. [데이터 엔지니어링] 지연 로딩(Lazy Loading) 대응을 위한 스크롤 및 반복 탐색
    # 이미지가 DOM에는 있지만 src가 아직 채워지지 않았거나, 화면 아래에 있을 때를 대비합니다.
    menu_url = None
    for i in range(5): # 최대 5번 시도
        print(f"🔎 메뉴판 탐색 중... (시도 {i+1}/5)")
        
        # 자바스크립트를 이용해 프로필 사진이 아닌 본문 메뉴판 이미지를 정밀하게 찾습니다.
        menu_url = driver.execute_script("""
            // 모든 이미지 태그를 가져옵니다.
            let imgs = document.querySelectorAll('img');
            for (let img of imgs) {
                // 필터링 조건: 
                // 1. 가로 크기가 300px 이상 (프로필 아이콘은 보통 100px 미만)
                // 2. 주소에 pstatic.net 또는 phinf.naver.net이 포함됨 (네이버 사진 서버)
                if (img.width > 300 && (img.src.includes('pstatic.net') || img.src.includes('phinf.naver.net'))) {
                    return img.src;
                }
            }
            return null;
        """)
        
        if menu_url:
            break
            
        # 못 찾았을 경우 아래로 스크롤하여 이미지 로딩을 유도합니다.
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

    # 5. 결과 확인 및 저장
    if menu_url:
        # 1. 사이즈 파라미터 강제 조정 (678x452 -> 750x452)
        # 금요일 메뉴까지 깨끗하게 나오도록 종환님이 찾아낸 최적값을 적용합니다.
        optimized_url = menu_url.replace("size=678x452", "size=750x452")
        
        print(f"\n🎯 최적화된 메뉴판 URL:\n{optimized_url}")
        
        # 2. 파일 저장
        with open("latest_menu_url.txt", "w", encoding="utf-8") as f:
            f.write(optimized_url)
        
    # 이제 이 optimized_url을 제미나이(app.py) 함수로 넘겨주면 됩니다!
    else:
        print("❌ 메뉴판 이미지를 찾지 못했습니다. 개발자 도구의 이미지 크기를 다시 확인해 주세요.")
        driver.save_screenshot("debug_capture.png")

except Exception as e:
    print(f"❌ 에러 발생: {e}")
finally:
    # 확인을 위해 잠시 대기 후 종료
    time.sleep(5)
    driver.quit()
import os
import pytest
import subprocess
from datetime import datetime
import shutil
import sys
import platform
from test_settings import BROWSERS, REPORT_ROOT

# 1. 建立主資料夾（日期命名）
timestamp = datetime.now().strftime("%Y-%m-%d")
timestamp_file = datetime.now().strftime("%H-%M-%S")
report_dir = os.path.join(REPORT_ROOT, timestamp)
os.makedirs(report_dir, exist_ok=True)

# 2. 建立 log 子資料夾
log_dir = os.path.join(report_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

# 3. 設定 Allure 及測試結果輸出資料夾
if platform.system() == "Windows":
    allure_cli = os.path.expanduser("~/scoop/apps/allure/current/bin/allure.bat")
else:
    allure_cli = "allure"  # Linux 上直接執行

if shutil.which(allure_cli) is None:
    print(f"❌ 找不到 Allure CLI：{allure_cli}")
    exit(1)


overall_exit_code = 0

for browser in BROWSERS:
    print(f"\n🔍 執行 {browser} 測試...")

    log_file = os.path.join(log_dir, f"{timestamp_file}_{browser}_log.txt")
    
    allure_raw = os.path.join(report_dir, f"allure-results_{browser}")
    allure_html = os.path.join(report_dir, f"allure-report_{browser}")
    os.makedirs(allure_raw, exist_ok=True)
    
    pytest_args = [
        "tests",
        "-v",
        f"--mybrowser={browser}",
        f"--alluredir={allure_raw}",           # ✅ Allure 測試中繼結果
        "--cov-report=term-missing",
        f"--log-file={log_file}"
    ]

    exit_code = pytest.main(pytest_args)

    # 4. 執行結束後，自動產生 Allure HTML 報告
    print("\n📊 產生 Allure 報告...")
    subprocess.run([allure_cli, "generate", allure_raw, "-o", allure_html, "--clean"], check=True)

    print(f"\n✅ Allure 報告已產生：{allure_html}")
    
    if exit_code != 0:
        print(f"❌ 測試未通過（{browser}）")
        overall_exit_code = 1  # ✅ 標記為失敗（但不馬上中止）

# 最後統一退出
if overall_exit_code != 0:
    print("❌ 測試總結：至少有一組瀏覽器測試失敗")
else:
    print("✅ 所有瀏覽器測試通過")

sys.exit(overall_exit_code)

index_file = os.path.join(allure_html, "index.html")

@echo off
set chrome_cookies_path=C:\Users\%username%\AppData\Local\Google\Chrome\User Data\Profile 1\Network\Cookies
set output_file=cookies_decrypted.txt
echo Decrypting Chrome cookies...
"ChromeCookiesView.exe" /decrypt_cookies "%chrome_cookies_path%" /scomma "%output_file%"
echo Done.
pause

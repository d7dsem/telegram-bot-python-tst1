# GIT usage on local PC 


On start
```
git init
git branch -M main // Створює гілку з ім'ям main (можна назвати й інакше)
git remote add github  https://github.com/d7dsem/telegram-bot-python-tst1.git // зв'язує локальний і віддалений репозиторії через ім'я 'github' (можна призначити інше)
```


While work
```
git add .
git commit -m "..."
git push -u github main

```


# Git on remote

Hard update
```
git fetch --all && git reset --hard github/main
```

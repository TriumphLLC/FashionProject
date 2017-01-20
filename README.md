### Установка плагина для Blender:

По адресу установленного блендера идем в папку `{номер версии}/scripts/addons/` и выполняем там:

```
ln -s {путь к репозиторию sp_market_manager_stable}/FashionProject/BlenderAddon/fashion_project
```
Например,
```
vmuser@my:~/Blender/2.77/scripts/addons$ ln -s ~/dev/sp_market_manager_stable/FashionProject/BlenderAddon/fashion_project
```

Далее в меню __File -> User Preferences -> Add-ons__, в __Supported Level__ выбираем __Testing__, включаем плагин __BPY: Fashion Project__.

Запуск файлов примеров из папки с блендером:

```
./blender ~/dev/sp_market_manager_stable/FashionProject/files/none.blend
```

```
./blender ~/dev/sp_market_manager_stable/FashionProject/files/points0.blend
```

# Задания 3-6

Первым делом нужно запустить базу данных: 
docker run -d --name wg_db -p 5432:5432 yzh44yzh/wg_forge_backend_env:1.1

Вторым делом нужно запустить контейнер с выполненным заданием: 
docker run -d -p 8080:80 --link wg_db:postgreDB skaborik/wg_backend_cats

Третьим делом послать запросы из заданий 3-6 по ссылке https://github.com/wgnet/wg_forge_backend

Готово, вы великолепны.

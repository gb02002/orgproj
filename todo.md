1. Сделать возможность отображения и раскрытия информации по отдельным транзакциям и подпискам. Предполагаю, что это надо сделать после подключения шлюза из-за более подробного понимая очередей, статусов, переводов и тд.



Сейчас надо проработать создание мок-шлюза.


08.02

    - refactor the main idea
    - mb make a new project 
    - think about quiz with fancy algorithm






    1. 
        The old idea were about wrong buisness idea. After summing up some info from aviasales director I decided to get rid of all billing methods, but pure transfering to org web.

        So, what do I have, what shell I delete and add:

            1) map stays
            2) I need to make quizz 
            3) Logging system is broke and useless. I will not have users at all. 

                I should have at least some of it, so the best and easiest dicision is to let people subscribe for their type of orgs and news. + I can test integration with mailing gate.

            4) There are no transaction model anymore. 


     I should make a new file, its much faster.a


     model list


     1. org. same as past
     2. loc same
     3. user. changed, simplier
     4. profile cut off
     5. trans same
     6. sub model, better to use it instead of messing with user model

     res;
     org, loc, user, sub

     good

     org + loc -> orgs app 
     user + sub -> user app

     noice


20.02

    Что я не перенес:
    main.views - видимо все для работы с отображением карты


17.03

    Добавить в представления в орг апп:
        фул инфо лок


    Проверить:
        Работу карты. Со стороны джанги все работает корректно.

    Add
        slug for orgs and list


    какие страницы почитать пока буду ехать назад
        45, 48, 61
        183
        205
        243
        268
        339

   

2103

    Доделать отображение всех локаций(можно без фильтров)

    Сделать план на завтра


2303
    
    Итак, надо доделать корректное изображение всех локакций на карте. 
        +- Надо убрать поп-ап на самой карте, он должен быть только в отдельном окне.
        + Проверить что отдает сервер   
        + Жалетельно сделать фильтрацию на стороне клиента
        + Реализовать фильтры
        - Сделать fullinfoloc
        - Добавить динамическое соотвествие фильтров через апи
        - Добавить сглаженое изменение, при перешелкивании фильтра оно слишком дергается. Желательно не менять картинку при неготовом рендере.

    Очередность работы: 3, 2, 4, 5, 1

    Прогресс:
        1. Ответы легкие - реализация на стороне клиента. Быстрее отклик, и все. Реализация postgres не очень интересная все равно
        2. Как реализовать фильтрацию?

            В клиент нам приходит список локаций. Мы его распаковываем и отрисовываем. 


        Оболочка json - 50 b. Каждый объетк весит ~150 байт. Это окей. 


2503
    
    Что надо сделать за сегодня: 

        Основное: 
        1. Реализовать fullinfo по клику на локу
        2. Подумать над listview для отображаемых локаций, аля googlemap
        3. Динамические фильтры 
        4* Не забыть подумать про оптимизацию карты, возможно в какой-то отдельный список todo на longterm. 



        Итак, новый день, новый бой с самим собой

        Я начну, скажу пару слов:

            1. fullinfo

                Что есть сейчас? Сейчас есть какая-то функция, которая работает через маркеры.


                Нужна функция, которая принимает список id, фетчит данные, распаковывает данные.
            
        ф0.1 отображение списка
            (
                ф1 фетч
                ф2 валидация, распаковка
                ф3 отображение
            )


        (!) Подумтаь над использованием HyperlinkedRelatedField вместо web и для org (!)

27.01
    
    Список на сегодня:
        1. Перелопатить логику вызова листов и маркеров, они должны делать не 2 запроса(bad optimization) по 2(логика)
        2. Динамические фильтры
        3. ?!?Взаимодействие с маркерами?!?

        1. Done +-
        
        2.  

            - api - просто получение json с filter-name filter-id
            - fetch(none) -> json -> inner-html 


31.03
     
    Успеть до утра пн

    1. Отображение орги
    2. 2 формы - обратная связь, добавление огри + смежные локации
    !3!. Рефакторинг + тесты
    4. Переделка нав бара
    5. Добавление языков
    
    Order: 1, 2, (3), 4 утром по расписанию, 5
    В перерыве читать current материалы на новые идеи.



        Adding stuff

        1. Org
        2. Location for existing org
        3. ?



01.04

    2 фичи: 
    
        1. Добавление пользователя, изначально для добавления новых записей. Также надо выдавать возможность изменения данных своей орги и локаций. 

        2. Просто добавление новых орг и локаций к ним с добавлением всей хуйни(формы и формсеты + права)


        Вид настроек для админов орг:

             for orgs -> main list of forms. 

    2 части вертикально. Верхняя - список орг под этим юзером. На этом же баре: ред, уд, добавление локи. При раскрытии(выпадающий список) - конкретные локи этой орги. Тоже кнопки, можно редачить.

    Нижняя - новая орга + лока formsets


<!--<script>-->
<!--var isLinkClickedLocation = false;-->

<!--function handleLocHeaderClick(event, locationId) {-->
<!--    if (!isLinkClickedLocation) {-->
<!--        toggleLocation(locationId);-->
<!--    }-->
<!--    isLinkClickedLocation = false;-->
<!--}-->

<!--function toggleLocation(locationId) {-->
<!--    var locationDetailsDiv = document.getElementById('location-details-' + locationId);-->
<!--    if (locationDetailsDiv.style.display === 'none') {-->
<!--        locationDetailsDiv.style.display = 'block';-->
<!--    } else {-->
<!--        locationDetailsDiv.style.display = 'none';-->
<!--    }-->
<!--}-->

<!--function handleLinkClickLocation(event) {-->
<!--    event.preventDefault();-->
<!--    isLinkClickedLocation = true;-->
<!--}-->

<!--var isLinkClickedMedia = false;-->

<!--function handlerMediaHeaderClick(event, mediaId) {-->
<!--    if (!isLinkClickedMedia) {-->
<!--        toggleMedia(mediaId);-->
<!--    } else {-->
<!--        handleLinkClickLocation(event); // Вызываем handleLinkClickLocation, чтобы ограничить toggleLocation-->
<!--    }-->
<!--    isLinkClickedMedia = false;-->
<!--}-->

<!--function toggleMedia(mediaId) {-->
<!--    var mediaDetailsDiv = document.getElementById('media-details-' + mediaId);-->
<!--    if (mediaDetailsDiv.style.display === 'none') {-->
<!--        mediaDetailsDiv.style.display = 'block';-->
<!--    } else {-->
<!--        mediaDetailsDiv.style.display = 'none';-->
<!--    }-->
<!--}-->
<!--</script>-->


<!--<div class="location" id="location-{{ location.pk }}" onclick="handleLocHeaderClick(event, {{ location.pk }})">-->
<!--            {{ location.location_name }}-->
<!--            &lt;!&ndash; Здесь можете добавить дополнительную информацию, которую нужно скрывать/показывать &ndash;&gt;-->

<!--            <div class="location-details" id="location-details-{{ location.pk }}" style="display: none;">-->
<!--                <ul>-->
<!--                    <li><strong>Address:</strong> {{ location.address }}</li>-->
<!--                    <li><strong>Open Hours:</strong> {{ location.open_hours }}</li>-->
<!--                </ul>-->
<!--                {% for media in location.media.all %}-->
<!--                <div class="media-info" onclick="handlerMediaHeaderClick(event, {{ media.media_id }})">-->
<!--                    {{ media.media_id }}-->
<!--                    <div class="media-details" id="media-details-{{ media.media_id }}" style="display: none;">-->


                

    14.04
    - дописать токены
    - перепроверить locmedia, подправить ссылки в choice-edit. 

    - начать работу с celery(не забыть про крон и mqrabbit). Просмотреть все что можно. Ответить на вопросы:
        
        % - что это?
        % - для чего, для чего нет? 
        % - Составить список что надо сделать с ним
        % - Установить и реализовать хотя бы один пункт? 


    15.04

        1. Redis: базовая инфа, что можно, как установаить, что нельзя, настроить кеш где надо.
        2. Редис как брокер соотбщений с celery.

    19 
        Добавить почту
        Рефакторинг + тесты

        Переделать сериализатор под чек выше верхнего. Все выступы сбрасываются до границы - максимум как полоска.
        add retrievelocationsfromcoordapiview

    20 
        Тесты: 3 view, serializers, ?db?
        Почта
        Начать celery

    23
        1. При регистрации отправить мне имеил
        2. Отчет за день. 
        3. Высылка критичных сообщений
        4. Небольшая веб-аналитика

        Morning. Tasks for today:
        
            1. Перерефакторить 6 view в один модульный
            2. Продумать middleware(просто стор вренени и путей хотя бы), создать пуш redis, разметить таблицу
            3. Подвязать это с celery

    24.
        1. Написать скрипт
        2. Разметить таблицу
        3. Подружить


    session_id: str
    path_info: str
    response_code: int
    time_for_response: float
    time_stamp: datetime
    User_Agent: str = ''
    ip_addr: str = ''
    referer: str = ''
    
    Разметка табоицы:



        CREATE TABLE stats;

    1. Cron
    2. gunicorn
    2. Docker(django + postgres + cron + external vals + redis + gunicorn)

    Gunicorn + nginx works, static works, postgres is populated by cron, celery works, smtp works, redis works, cache works.

    25.
        
        resols:
            1. Find out how systemd works, how and what should become deamons, other .sh and basic ci/cd. All should work automatically after reboot, zero movements.
            2. DOOOOOOOOOOOOOOCCKEERRRRRRRRRRRRRRR COMPOSE ))))))))))))
            3. testssssss)

            
            Утро: 
            1) ABC
            2) рефакторинг(db, allas)
            3) тесты
            4)env

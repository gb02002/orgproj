# Dev-Journal

#### This file describes a bit of inside thoughts during my development. Basically, it is my log-book.

Is has simple structure: small chapter name and date. It is not clean since I want to show it as raw as possible. Perhaps you can find something interesting and useful for yourself here, or notice some mistake of mine and let me know where my logic went wrong.

My current comments would be in normal style, while notes would be in basic code format.
## First attempt. 02.12.2023

### Start

Here I set a list of tech I will use:

	Heeeello!!!
	
	This is README for a webapp used for managing Charity organizations. I am a student in the Netherlands, so this app will work specifically for this country. 
	
	By so far I will use this file for basic documentation: todo-list, plan, dates, as notes and some applications manual. At the end all of it will be removed to aseparate file with specifical technical information, so this file will look more alike README.
	
	This is the list of technologies I am planning to use:
	    - Python(3.12)
	    - Django(4.2.4)
	    - Postgesql
	    - Docker
	    - Celery
	    - Nginx
	    - etc
	

Unlike the final design, the original idea also had a payment gateway in it. Later on, I abandoned this idea. This was due to difficulties with registering with Stripe and Paypal. Since the main project I was considering as a reference was aviasales.ru, soon after the problems I got acquainted with their business model and realized that they do not work with clients' money directly, but work only as an aggregator, so I abandoned this idea.


	Overview:

    So, what I want to make. 
        1. Main page: on the main page you can see the scalling map, and the charity organisations on it. On tap more info will expand: name, focus, amounts, working hours, etc. Will be nice to add some filters too. 
        2. Auto month donation(spec or with lowest budget).
            With the lowest budget system will chose randomly one?! org with the poorest situation at the end of the month and will contrubute with all subs of this kind.


This is declaration of entites I have in proj, models I would need and Django apps ofr them:

	At the start I will focus on 5 entities(MVP): 

    1. User: App should work with 2 types of users: registered and non. Non registered can look through all info. Registered should have additional profile with supply info, sharing, history etc. 
    2. Orgs: I will work with all types of charity organizations. Each org will have some metadata and interactive data, such as filters(category), mail, phone, name, extra resources, budget(grey, green, yellow, red), news, etc. 
    3. Contribution/transaction. Users can donate via the site, some fee will apply(? depends if it counts as commercial activity). 
    4. Subscription. 
    5. Profile. Users can change their private info, payment details, can add some SM to share donations and so on. 
    
	List of apps:
	    1. Main: it will include all orgs info and mapping.
	    2. Users: user and profile.
	    3. Payment-logic aka transactions: subs, history, transaction logic, billing, etc.


	List of needed tables:

    1. User(users app):
        
        username - email
        password - password
        user_id - pk
        time_created
        last_active 


    2. Profile(users app):
        
        user_id(OnetoOne)
        name
        surname
        phone
        history(transaction_ids)
        subs - enum(not sure)
 
    3. Org(org app):
        
        org_id
        title
        desc
        mail
        phone
        web
        current budget
        desired budget
        bank details(IBAN)
        tikkie link(if permanent, blank=True)


    4. History(user app)

        transaction_id - pk
        user_id(OneToOne)
        time_creation 
        address - org_id(cause of diff payment ways)
        amount - float
        is_subscription - bool

    5. Subscriptions(transaction app):

        Each user may have multiple subs, so it is easyer to make a separate db for them.

        Types of subsciption:
            1. Specified 
            2. System choise

        sub_pk(will be stored in sub of user) 
        user_id(ManyToOne)
        org_id
        current_period_start 
        current_period_end - blank=True 
        sub_type - bool(spec or lowest) 
        amount - float

    6. GeoData:
        Idk how to work with geodata at all. 
        This model will be connected to Org db by ForeignKey

Conclusion on first part:

	Thigs to consider:
	1. Address of billing
	2. I need one more model to work with map. Org model looks big enough already, so I will use separete model to work with map.
	3. Phone storage. 
	Main country to work with is nl. Fuck that. 99% will be standart dutch nums, so before work they will be validated. Storing as plain char.
	1. Mb i don't need the history field in profile. The only reason to have it is that it makes it to search faster as we search by set of pks. -\w/-


### Roadmap part

	Here's the approximate roadmap I got:

	1. Establish database (main skeleton, all models, routes, users, basic organization filtering, tests, validators)
	2. GeoDjango: Set up correct model, configure validation, ForeignKey relationships, tests
	3. Mapping:
	    - Option 1: Using a library like Leaflet. Custom map, custom display.
	    - Google API.
	4. Asynchronous tasks
	5. Celery, Redis
	6. Cache, sessions
	7. Understanding the need for any frontend. If yes, then:
	    - 8) Writing REST API
	    - 9. Integrating Vue.js, React, or Angular
	8. Transactions
	9. Daily, monthly tasks
	10. Nginx, gunicorn
	11. Docker, docker compose
	12. Deployment, deployment tests, automatic deployment, logging storage and sending, HTTPS
	13. Database population
	14. Official registration
	15. release


07.12:

    1)Models base are finished. The next step is to add everything around them:
        
        1. Forms +
        2. Tests -
        3. Managers +

    2)After it base logic:
        
       1. VIews +
       2. Paths +
       3. templates, etc +-
        

08.12

	1. Base profile logic implemented.
	2. Got stuck with profile editing (I'm an idiot). 
	3. Currently, I'll implement a basic profile editor. In the future, I need to come back and implement editing on the same page with a request type switch to POST via a JS script and sending JSON via JQuery (or some similar alternative I'll hook up). Right now, I'm screwing around with it.
	    

	Tasks for this evening:
	
	1. Implement a minimal taskbar in base.html.
	2. Implement validators and attach them to the HTML.
	3. Consider whether anything needs to be done with tests (for userapp).
	4. GeoDjango. Understand what to do with the Location model.
	5. Finish out the design skeleton in Figma. +-
	6. Specifically plan the routing. +



10.12:
    
    Task for today:
        1. Install GeoDjango
        2. Finish Locations model
            consider validators and all relaited stuff
        3. Install PostGIS
        4. If time:
            read pytest


12.12:
	
	- The first things to acquaint oneself with in the context of basic theory:
	    
	    1. Doc PostGIS
	    2. Google API
	    3. Finish watching the web scraping course
	- Questions I need to answer today:
	    
	    1. How different is working with a custom map versus using a third-party API?
	    2. What types of objects exist? How do they interact, what are the basic functions?
	    3. How is data storage organized?
	    4. How do map APIs work, how is interactive display achieved?
	    5. How to organize storage of objects. K-means, groups, indexing, etc.


### Maps. 16.12.2023

On this part I decided to focus on Map part since it is a core function and has lots ways of implementation. A lot of thoughts here are arisen and falls during one day, so most of it is just thoughts around a topic with attempts to find a good way to start work. 


	- Base map should have 2 possible forms(layout):
	    1. Sipmle view. Only city, district names, main aves and org names.
	    2. More complex aka normal google view. Idk if client should have a choice to choose layout, but i dont like basic view of google in my proj.
	
	- Markers customize:
	    https://developers.google.com/maps/documentation/javascript/advanced-markers/graphic-markers?hl=ru
	    Good idea to make own markers for different types of orgs(filter-based)
	

	After some research I think I came out with some approx way of realization:
	    1. Client makes a query.
	    2. From base js he recieves base 

 Basically this way is a normal DRF app using AJAX. 

This is a list of issues I spend time to fix: 

	1. Finish base of cluster script
    2. Раскидать основые функциональныее элементы отображения по map url. Сноска, легенда, значки, хуемое, слои, приближение, streetview, expand, raster desable
    3. 

    js scritp(map instance async)
    подумать про медиафайлы

	Issuies to consider:
	    1. Geolocation. By server or map itself? Idk, seems map inself. Tbraded. I think tons of info and implementation.
	    2. Where to render markers. Mb we dont even need to send them.


	logic of get_bounded_locations:
    
    1. difining area.
    2. get cluster in order: middle, corners


Here I come to point where I was searching for different points searching approaches. More info you can find on [Analytics report][] page.

	Approaches to retrieving geodata from the database: 
	1 - Ignore searching by coordinates, simply properly mark the territory and retrieve by cluster. 
	2 - Obtain a rectangle. 
		2.1 Ignore clusters and just run all points through containment. 
		2.2 Do not ignore clusters, determine it and, considering the cluster, retrieve everything needed.
	
	3 - Read coordinates. If the entire area is one cluster, simply return it. If not, return the area, as there can be a maximum of 4 clusters at once.
	4 - Obtain an area. Search for the occurrence of one object. Based on it, determine which cluster it belongs to. Return to the view, continue searching for the rest to ensure that there is only one cluster. If not, return the remaining for rendering.


22.12.23

	Beginning of the day. Here's what I'll start with:
	   1. Basic tests are written for db_utils, apiviews, serializers.
	   2. There's a basic connection with the database and JS. Objects somehow render.
	
	First: Filters. Implement basic JS, accept and filter on the backend.
	Second: Views for lists. Same logic can be attached there.
	Third: Admin panel.
	
	1. Filters:
	   The script has a list of filters. Later, it seems like it can be separated because there are several pages + cache. There are just tile objects, 2 states.
	
	   Implementation options:
	      1) If the coordinates are the same, then when updating filters, there are two options: either update the query, or immediately retrieve all objects and filter the render on the frontend. As if the second option is generally better in the general case, since the number of queries to the database is more important. Probably it's right to limit by area, if more than x then add a filter to the query.
	
	   After reading materials, I suppose I'll have to change the query type to post and fetch all locations. The upper limits of the request weight are around 0.2 KB, which is not so much. Filtering will be only on the frontend. This way it will work simply. If there are performance issues later, I'll think about it. \(>__<)/
	
	Functions for map:
	1. get bounds
	2. fetch
	3. initmap
	4. applyfilter
	5. map sets
	6. debounce
	7. clear
	8. renderpoints

## Cleaning ends.

In this part I realized that transactions, history, payment gateway is not a good idea.


08.01

    - refactor the main idea
    - mb make a new project 
    - think about quiz

    1. 
        The old idea were about wrong buisness idea. After summing up some info from aviasales director I decided to get rid of all billing methods, but pure transfering to org web.

        So, what do I have, what shell I delete and add:

            1) map stays
            2) Logging system is broke and useless. I will not have users at all. 

                I should have at least some of it, so the best and easiest dicision is to let people subscribe for their type of orgs and news. + I can test integration with mailing gate.

            3) There are no transaction and history model anymore. 

     I should make a new file, its much faster.

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



It was a transfer to new project.

14.02

	Today I need to set up all base parts of project. I have main components from my old one, so I should just make it work together. 
	
	plan: 
	1. Filling all requirements and dependencies.
	2. Settings
	3. Db with docker. Check geos, gdal etc
	4. hmm
	
	
	1. Base is working. Now I need to make all tuning I need. 
	Should I specify here the list? I guess it will be better.


18.02

    Models are designed, the table works, the server starts.

	Now we need to transfer what we can, namely:
	
	1. Paths
	2. Templates
	3. Map (separately)
	4. CSS HTML
	
	Today we need to deal with everything except the map - cool. There's too much and a lot has changed.
	
	The content is being served. The problem is with the display of HTML. The structure needs to be redone into proper lists.


The pages are taken from Mele Django book(4th edition). 

17.02

    Add to org app view:
        full_info_location


    Check:
		Work of map. From Django side in works okay.

    Add
        slug for orgs and list


    Pages to read:
        45, 48, 61
        183
        205
        243
        268
        339

### New chapter

21 02:
	
	   Complete the display of all locations (can be without filters).
	
23 02:
	
	   So, it is necessary to finish the correct display of all locations on the map.
	       +- The pop-up on the map itself needs to be removed; it should only be in a separate window.
	       + Check what the server returns
	       + It is advisable to implement client-side filtering
	       + Implement filters
	       - Make fullinfoloc
	       - Add dynamic correspondence of filters via the API
	       - Add smooth transition when switching filters; it jerks too much. It is preferable not to change the image when rendering is not complete.
	
	   Work sequence: 3, 2, 4, 5, 1
	
	   Progress:
	       1. Client-side implementation - easy responses. Faster response, that's all. Implementation in PostgreSQL is not very interesting anyway.
	       2. How to implement filtering?
	           We receive a list of locations on the client. We unpack it and render it.
	
	   JSON shell - 50 B. Each object weighs ~150 bytes. This is okay.


25 02:

	What needs to be done for today:

	Main tasks:
	1. Implement fullinfo on click on the location.    
	2. Think about listview for displayed locations, like Google Maps.    
	3. Dynamic filters.    
	4. Don't forget to think about map optimization, maybe put it in some separate long-term to-do list.`
	
	1. Fullinfo
	What do we have now? Right now, there is some function that works through markers.         We need a function that takes a list of IDs, fetches data, and unpacks the data.     
	f0.1 Displaying the list
	(            
	f1 fetch
	f2 validation, unpacking            
	f3 display        
	)     
	
	(!) Think about using HyperlinkedRelatedField instead of web and for org (!)`

30.02

	Today's to-do list: 
	1. Rework the logic of calling lists and markers; they should not make 2 requests (bad optimization) per 2 (logic). 
	2. Dynamic filters. 
	3. ?!?Interacting with markers?!?


03.03

	Deadline by Monday morning.
	
	1. Displaying organizations
	2. 2 forms - feedback, adding organization + related locations !3!. Refactoring + tests
	3. Navbar redesign
	4. Adding languages
	
	Order: 1, 2, (3), 4 in the morning as scheduled, 5 Read current materials for new ideas during breaks.
	
	Adding stuff:
	
	1. Org
	2. Location for existing org
	3. ?


### Close to end

05.04

	2 features:
	
	1. User addition, initially for adding new entries. Also need to provide the ability to change their organization's and locations' data.
	    
	2. Just adding new organizations and locations to them with all the necessary stuff (forms and formsets + permissions).
	    
	
	Settings view for organization admins:

	`for orgs -> main list of forms.`
	
	2 sections vertically. The upper section - list of organizations under this user. On this bar: edit, delete, add location. When expanded (dropdown list) - specific locations of this organization. Buttons as well, can be edited.
	
	The lower section - new organization + location formsets.

14.04

	- Complete tokens
	    
	- Double-check locmedia, fix links in choice-edit.
	    
	- Start working with Celery (don't forget about cron and mqrabbit). Review everything possible. Answer the questions:
	    
	    % - What is it? % - What is it for, what is it not for? % - Create a list of what needs to be done with it % - Install and implement at least one item?
    

15.04

	1. Redis: basic info, what it can do, how to install, what it can't do, configure cache where needed.
	2. Redis as a message broker with Celery.

19.04

	 Add email Refactoring + tests
	Redo bounds serializer to check above the top. All protrusions are reset to the border - maximum as a stripe. add retrievelocationsfromcoordapiview


20.04 

	Tests: 3 views, serializers, ?db? Email Start Celery

23.04 

	1. Send me an email upon registration 
	2. Daily report. 
	3. Send critical messages 
	4. Small web analytics

	Morning. 
	Tasks for today: 
	1. Refactor 6 views into one modular 
	2. Consider middleware (at least store time and paths), create Redis push, map the table 
	3. Integrate this with Celery

24.04  

	1. Write a script 
	2. Map the table 
	3. Integrate

    session_id: str
    path_info: str
    response_code: int
    time_for_response: float
    time_stamp: datetime
    User_Agent: str = ''
    ip_addr: str = ''
    referer: str = ''
    
    Table:
        CREATE TABLE stats;

    1. Cron
    2. gunicorn
    2. Docker(django + postgres + cron + external vals + redis + gunicorn)

    Gunicorn + nginx works, static works, postgres is populated by cron, celery works, smtp works, redis works, cache works.


Here I were not satisfied with what I have with Add/Edit/Del for Loc/Org/Media, so ABC was meant to help me with it. It didn't work out(

 25.04
        
	resols:
		1. Find out how systemd works, how and what should become deamons, other .sh and basic ci/cd. All should work automatically after reboot, zero movements.
		2. docker compose
		3. tests

	Morning:
	
	1. ABC -
	2. Refactoring (db, allas)
	3. Tests
	4. Env
	5. Add slave cache on Redis



29.04 

	1. General media volume 
	2. User tests 
	3. Add check for web_stats 
	4. Redo all CSS 
	5. Complete simple profile
	6. Add Celery tasks for adding (signals+-)
	
	(1 + 3), 2, 5, 4, 6


## Final

Here most of logs are about setting up VPS

11.05

	1. Create Dockerfile for db + 
	2. clean up + 
	3. logging(?) + 
	4. pg_dump + 
	5. Daemonization + 
	6. Configure two types of locales
	7. Clean up logging as well
	8. Finalize Redis
	9. Fix trans on about. Add information there, reconfigure localization, add a second page for about.
	10. Finally configure SMTP

That is it

Then most of logs are about configuring iptables, passing variables from 1 file, making scripts, making daemons etc. 

Hope it would help you!

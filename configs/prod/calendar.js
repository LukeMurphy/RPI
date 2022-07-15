<apex:page controller="DCTV_Calendar_Controller" standardStylesheets="false" showHeader="false">
    <apex:pageBlock >
        <style>
        .cld-main{
            width: auto;
            font-family: 'Roboto Condensed', sans-serif;
            background-color:#ffffff;
        }
        .cld-main a{
            display:block;
            border-top:1px solid #efefef;
            color: #111111;
            text-decoration: none;
            background-color: #222222;
            padding: 1px;
        }
       
        .cld-datetime{
            position: relative;
            width: 66%;
            min-width: 100px;
            max-width: 300px;
            margin: auto;
            overflow: hidden;
        }
        .cld-datetime .today{
            position: relative;
            float: left;
            width: calc(100% - 40px);
            margin: auto;
            text-align: center;
        }
        .cld-nav{
            position: relative;
            width: 20px;
            height: 20px;
            margin-top: 2px;
        }
        .cld-nav:hover{
            cursor: pointer;
        }
        .cld-nav:hover svg{
            fill: #666;
        }
        .cld-rwd{
            float: left;
        }
        .cld-fwd{
            float: right;
        }
        .cld-nav svg:hover{
        }
        .cld-labels, .cld-days{
            padding-left: 0;
        }
        .cld-label, .cld-day{
            box-sizing: border-box;
            display: inline-block;
            width: 14.28%;
            text-align: center;
        }
        .cld-day{
            display: block;
            float: left;
            position: relative;
            margin: 0;
            padding: 0px;
            height: 170px;
            border: 1px solid #ddd;
            overflow-y: auto;
            background-color:#ffffff;
        }
        .cld-day.clickable:hover{
            cursor: pointer;
        }
        .cld-day.today{
            border: 1px solid #0000FFaa;
            background-color: #efefef;
        }
        .cld-day.disableDay{
            opacity: 0.5;
        }
        .cld-day.nextMonth, .cld-day.prevMonth{
            opacity: 0.33;
        }
        .cld-number{
            margin: 0;
            text-align: left;
        }
        .cld-title{
            font-size: 10px;
            display: block;
            margin-top:.5em;
            margin-right: 0px;
            font-weight: normal;
            width: 100%;
        }
        .cld-day:hover{
            background: #eee;
        }
        .cld-number.eventday{
            font-weight: bold;
        }
        .cld-number.eventday:hover{
            background: #eee;
        }
        .today .cld-number.eventday:hover{
        }
        
        body{
            font-family: Calibri, sans-serif;
            font-family: 'Roboto Condensed', sans-serif;
            color: #333;
            background: #ffffff;
        }
        
        .bodyStyle {
            font-family: Calibri, sans-serif;
            font-family: 'Roboto Condensed', sans-serif;
            color: #333;
            background: #ffffff;
        }
        
        .brandQuaternaryBgr {
            background-color:#ffffff;
        }

        </style>
        
        <script>
        /*
        Author: Jack Ducasse;
        Version: 0.1.0;
        (◠‿◠✿)
        */
        
        // dark
        styleArray = ["#943126","#1a5276","#0e6655","#5b2c6f","#935116","#9c640c"];
        
        // light
        styleArray = ["#fae5d3","#fcf3cf","#d1f2eb","#d4e6f1","#ebdef0","#f2d7d5"];   
        
        var Calendar = function(model, options, date){
        // Default Values
        this.Options = {
            Color: '',
            LinkColor: '',
            NavShow: true,
            NavVertical: false,
            NavLocation: '',
            DateTimeShow: true,
            DateTimeFormat: 'mmm, yyyy',
            DatetimeLocation: '',
            EventClick: '',
            EventTargetWholeDay: false,
            DisabledDays: [],
            ModelChange: model
        };
        // Overwriting default values
        for(var key in options){
            this.Options[key] = typeof options[key]=='string'?options[key].toLowerCase():options[key];
        }
        model?this.Model=model:this.Model={};
        this.Today = new Date();
        this.Selected = this.Today
        this.Today.Month = this.Today.getMonth();
        this.Today.Year = this.Today.getFullYear();
        if(date){this.Selected = date}
        this.Selected.Month = this.Selected.getMonth();
        this.Selected.Year = this.Selected.getFullYear();
        this.Selected.Days = new Date(this.Selected.Year, (this.Selected.Month + 1), 0).getDate();
        this.Selected.FirstDay = new Date(this.Selected.Year, (this.Selected.Month), 1).getDay();
        this.Selected.LastDay = new Date(this.Selected.Year, (this.Selected.Month + 1), 0).getDay();
        this.Prev = new Date(this.Selected.Year, (this.Selected.Month - 1), 1);
        if(this.Selected.Month==0){this.Prev = new Date(this.Selected.Year-1, 11, 1);}
        this.Prev.Days = new Date(this.Prev.getFullYear(), (this.Prev.getMonth() + 1), 0).getDate();
        };
        function createCalendar(calendar, element, adjuster){
        if(typeof adjuster !== 'undefined'){
        var newDate = new Date(calendar.Selected.Year, calendar.Selected.Month + adjuster, 1);
        calendar = new Calendar(calendar.Model, calendar.Options, newDate);
        element.innerHTML = '';
        }else{
        for(var key in calendar.Options){
        typeof calendar.Options[key] != 'function' && typeof calendar.Options[key] != 'object' && calendar.Options[key]?element.className += " " + key + "-" + calendar.Options[key]:0;
        }
        }
        var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        function AddSidebar(){
        var sidebar = document.createElement('div');
        sidebar.className += 'cld-sidebar';
        var monthList = document.createElement('ul');
        monthList.className += 'cld-monthList';
        for(var i = 0; i < months.length - 3; i++){
        var x = document.createElement('li');
        x.className += 'cld-month';
        var n = i - (4 - calendar.Selected.Month);
        // Account for overflowing month values
        if(n<0){n+=12;}
        else if(n>11){n-=12;}
        // Add Appropriate Class
        if(i==0){
        x.className += ' cld-rwd cld-nav';
        x.addEventListener('click', function(){
        typeof calendar.Options.ModelChange == 'function'?calendar.Model = calendar.Options.ModelChange():calendar.Model = calendar.Options.ModelChange;
        createCalendar(calendar, element, -1);});
    x.innerHTML += '<svg height="15" width="15" viewBox="0 0 100 75" fill="rgba(255,255,255,0.5)"><polyline points="0,75 100,75 50,0"></polyline></svg>';
    }
    else if(i==months.length - 4){
    x.className += ' cld-fwd cld-nav';
    x.addEventListener('click', function(){
    typeof calendar.Options.ModelChange == 'function'?calendar.Model = calendar.Options.ModelChange():calendar.Model = calendar.Options.ModelChange;
    createCalendar(calendar, element, 1);} );
x.innerHTML += '<svg height="15" width="15" viewBox="0 0 100 75" fill="rgba(255,255,255,0.5)"><polyline points="0,0 100,0 50,75"></polyline></svg>';
}
else{
    if(i < 4){x.className += ' cld-pre';}
    else if(i > 4){x.className += ' cld-post';}
    else{x.className += ' cld-curr';}
    //prevent losing var adj value (for whatever reason that is happening)
    (function () {
        var adj = (i-4);
        //x.addEventListener('click', function(){createCalendar(calendar, element, adj);console.log('kk', adj);} );
        x.addEventListener('click', function(){
        typeof calendar.Options.ModelChange == 'function'?calendar.Model = calendar.Options.ModelChange():calendar.Model = calendar.Options.ModelChange;
        createCalendar(calendar, element, adj);} );
        x.setAttribute('style', 'opacity:' + (1 - Math.abs(adj)/4));
        x.innerHTML += months[n].substr(0,3);
    }()); // immediate invocation
    if(n==0){
        var y = document.createElement('li');
        y.className += 'cld-year';
        if(i<5){
            y.innerHTML += calendar.Selected.Year;
        }else{
            y.innerHTML += calendar.Selected.Year + 1;
        }
        monthList.appendChild(y);
    }
}
monthList.appendChild(x);
}
sidebar.appendChild(monthList);
if(calendar.Options.NavLocation){
document.getElementById(calendar.Options.NavLocation).innerHTML = "";
document.getElementById(calendar.Options.NavLocation).appendChild(sidebar);
}
else{element.appendChild(sidebar);}
}
var mainSection = document.createElement('div');
mainSection.className += "cld-main";
function AddDateTime(){
var datetime = document.createElement('div');
datetime.className += "cld-datetime";
if(calendar.Options.NavShow && !calendar.Options.NavVertical){
var rwd = document.createElement('div');
rwd.className += " cld-rwd cld-nav";
rwd.addEventListener('click', function(){createCalendar(calendar, element, -1);} );
rwd.innerHTML = '<svg height="15" width="15" viewBox="0 0 75 100" fill="rgba(0,0,0,0.5)"><polyline points="0,50 75,0 75,100"></polyline></svg>';
datetime.appendChild(rwd);
}
var today = document.createElement('div');
today.className += ' today';
today.innerHTML = months[calendar.Selected.Month] + ", " + calendar.Selected.Year;
datetime.appendChild(today);
if(calendar.Options.NavShow && !calendar.Options.NavVertical){
var fwd = document.createElement('div');
fwd.className += " cld-fwd cld-nav";
fwd.addEventListener('click', function(){createCalendar(calendar, element, 1);} );
fwd.innerHTML = '<svg height="15" width="15" viewBox="0 0 75 100" fill="rgba(0,0,0,0.5)"><polyline points="0,0 75,50 0,100"></polyline></svg>';
datetime.appendChild(fwd);
}
if(calendar.Options.DatetimeLocation){
document.getElementById(calendar.Options.DatetimeLocation).innerHTML = "";
document.getElementById(calendar.Options.DatetimeLocation).appendChild(datetime);
}
else{mainSection.appendChild(datetime);}
}
function AddLabels(){
var labels = document.createElement('ul');
labels.className = 'cld-labels';
var labelsList = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
for(var i = 0; i < labelsList.length; i++){
var label = document.createElement('li');
label.className += "cld-label";
label.innerHTML = labelsList[i];
labels.appendChild(label);
}
mainSection.appendChild(labels);
}
function AddDays(){
// Create Number Element
function DayNumber(n){
var number = document.createElement('p');
number.className += "cld-number";
number.innerHTML += n;
return number;
}
var days = document.createElement('ul');
days.className += "cld-days";
// Previous Month's Days
for(var i = 0; i < (calendar.Selected.FirstDay); i++){
var day = document.createElement('li');
day.className += "cld-day prevMonth";
//Disabled Days
var d = i%7;
for(var q = 0; q < calendar.Options.DisabledDays.length; q++){
if(d==calendar.Options.DisabledDays[q]){
day.className += " disableDay";
}
}
var number = DayNumber((calendar.Prev.Days - calendar.Selected.FirstDay) + (i+1));
day.appendChild(number);
days.appendChild(day);
}
// Current Month's Days
for(var i = 0; i < calendar.Selected.Days; i++){
var day = document.createElement('li');
day.className += "cld-day currMonth";
//Disabled Days
var d = (i + calendar.Selected.FirstDay)%7;
for(var q = 0; q < calendar.Options.DisabledDays.length; q++){
if(d==calendar.Options.DisabledDays[q]){
day.className += " disableDay";
}
}
var number = DayNumber(i+1);
// Check Date against Event Dates
for(var n = 0; n < calendar.Model.length; n++){
var evDate = calendar.Model[n].Date;
var toDate = new Date(calendar.Selected.Year, calendar.Selected.Month+1, (i+1));
if(evDate.getTime() == toDate.getTime()){
number.className += " eventday";
var title = document.createElement('span');
title.className += "cld-title";
if(typeof calendar.Model[n].Link == 'function' || calendar.Options.EventClick){
var a = document.createElement('a');
a.setAttribute('href', '#');
a.innerHTML += calendar.Model[n].Title;
if(calendar.Options.EventClick){
var z = calendar.Model[n].Link;
if(typeof calendar.Model[n].Link != 'string'){
a.addEventListener('click', calendar.Options.EventClick.bind.apply(calendar.Options.EventClick, [null].concat(z)) );
if(calendar.Options.EventTargetWholeDay){
day.className += " clickable";
day.addEventListener('click', calendar.Options.EventClick.bind.apply(calendar.Options.EventClick, [null].concat(z)) );
}
}else{
a.addEventListener('click', calendar.Options.EventClick.bind(null, z) );
if(calendar.Options.EventTargetWholeDay){
day.className += " clickable";
day.addEventListener('click', calendar.Options.EventClick.bind(null, z) );
}
}
}else{
a.addEventListener('click', calendar.Model[n].Link);
if(calendar.Options.EventTargetWholeDay){
day.className += " clickable";
day.addEventListener('click', calendar.Model[n].Link);
}
}
title.appendChild(a);
}else{
title.innerHTML += '<a href="' + calendar.Model[n].Link + '" style="background-color:' + styleArray[calendar.Model[n].style] + '">' + calendar.Model[n].Title + '</a>';
}
number.appendChild(title);
}
}
day.appendChild(number);
// If Today..
if((i+1) == calendar.Today.getDate() && calendar.Selected.Month == calendar.Today.Month && calendar.Selected.Year == calendar.Today.Year){
day.className += " today";
}
days.appendChild(day);
}
// Next Months Days
// Always same amount of days in calander
var extraDays = 13;
if(days.children.length>35){extraDays = 6;}
else if(days.children.length<29){extraDays = 20;}
for(var i = 0; i < (extraDays - calendar.Selected.LastDay); i++){
var day = document.createElement('li');
day.className += "cld-day nextMonth";
//Disabled Days
var d = (i + calendar.Selected.LastDay + 1)%7;
for(var q = 0; q < calendar.Options.DisabledDays.length; q++){
if(d==calendar.Options.DisabledDays[q]){
day.className += " disableDay";
}
}
var number = DayNumber(i+1);
day.appendChild(number);
days.appendChild(day);
}
mainSection.appendChild(days);
}
if(calendar.Options.Color){
    mainSection.innerHTML += '<style>.cld-main{color:' + calendar.Options.Color + ';}</style>';
}
if(calendar.Options.LinkColor){
    mainSection.innerHTML += '<style>.cld-title a{color:' + calendar.Options.LinkColor + ';}</style>';
}
element.appendChild(mainSection);
if(calendar.Options.NavShow && calendar.Options.NavVertical){
    AddSidebar();
}
if(calendar.Options.DateTimeShow){
    AddDateTime();
}
AddLabels();
AddDays();
}
function calendarInit(el, data, settings){
    var obj = new Calendar(data, settings);
    createCalendar(obj, el);
}
</script>
<div id="calendar"></div>
<script>
var eventsArray = [<apex:outputText value="{!s}"></apex:outputText>];

var loc = window.top.parent.location.href;
var locParts = loc.split("?");


// sort by name
eventsArray.sort(function(a, b) {
  var nameA = a.Title.toUpperCase(); // ignore upper and lowercase
  var nameB = b.Title.toUpperCase(); // ignore upper and lowercase
  if (nameA < nameB) {
    return -1;
  }
  if (nameA > nameB) {
    return 1;
  }
  // names must be equal
  return 0;
});

function stringReplacer(match, part1, part2, part3, part4) {
    return part1 + part2 + "<br />" + part3;
}

currentTitle = "";
count = -1;
for( e in eventsArray) {
    titleParts = eventsArray[e].Title.split("&");
    titlePart = titleParts[0];
    if (titlePart != currentTitle) {
        count++;
        currentTitle = titlePart;
        if (count > 5) {
            count = 0;
        }
    }
    
    // Assign a style number to each course
    eventsArray[e].style = count;
    
    // Clean up the title for readability
    //eventsArray[e].Title = eventsArray[e].Title.slice(4);
    eventsArray[e].Title = eventsArray[e].Title.replaceAll("&nbsp\;","");
    eventsArray[e].Title = eventsArray[e].Title.replaceAll("&nbsp","");
    eventsArray[e].Title = eventsArray[e].Title.replace(/(Session\s)([0-9])(\s)/, stringReplacer);
}

var len = eventsArray.length;
// remove non public events


for(i=0;i<len;i++) {
    if (locParts.length == 1 ) {
        if (eventsArray[i].view == "nonpublic") {
            eventsArray[i].Title = "";
            eventsArray[i].Date = new Date(1900,1,1);
        }
    }
}

function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

var delayCalenderInit = false;
var loc = window.top.parent.location.href;
var locParts = loc.split("?");
if (locParts.length > 1) {
    if (locParts[1] == "internalcalendar=show") {
        delayCalenderInit = true;
        document.write('<style>.cld-day{height:300px}</style>');
        readTextFile("https://prod1.agileticketing.net/websales/feed.ashx?guid=d1578bde-e18f-41e1-a3bb-b2244647d15a&showslist=true&withmedia=true&format=json&v=latest&", function(text) {
            var data = JSON.parse(text);
            var l = 0;
            if (data.ArrayOfShows != undefined) {
                l = data.ArrayOfShows.length;
            }
            
            for (i = 0; i < l; i++) {
                //console.log(data.ArrayOfShows[i]['Name'])
                l2 = data.ArrayOfShows[i]['CurrentShowings'].length;
            
                for (ii = 0; ii < l2; ii++) {
                    rawTime = data.ArrayOfShows[i]['CurrentShowings'][ii]['StartDate'].split("T");
                    rawTimeEnd = data.ArrayOfShows[i]['CurrentShowings'][ii]['EndDate'].split("T");
                    timeSections = rawTime[0].split("-");
                    timeSectionsEnd = rawTimeEnd[0].split("-");
                    eventsArray.push( {'Date': new Date(timeSections[0], timeSections[1], timeSections[2]), 
                    'Title': data.ArrayOfShows[i]['Name'] + " \n<br/>" + data.ArrayOfShows[i]['CurrentShowings'][ii]['Venue']['Name'] + " \n<br/>" + rawTime[1].substring(0, 5) + " - " + rawTimeEnd[1].substring(0, 5) , 
                    'Link': '#', 
                    'style':5},);
                }
            }
            var settings = {};
            var element = document.getElementById('calendar');
            calendarInit(element, eventsArray, settings);
        });
    }
}


// if the AgileTix feed has to be loaded, wait until that is done
// before initiating the calendar - otherwise those events won't
// show up on the first load


if (delayCalenderInit == false) {
    var settings = {};
    var element = document.getElementById('calendar');
    calendarInit(element, eventsArray, settings);
}

</script>
</apex:pageBlock>
</apex:page>
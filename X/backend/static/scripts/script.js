const url = 'https://api.covid19india.org/data.json';
var active_cases_perc;
var deaths_today_perc;
var vaccine_perc;

async function getData(callback) {
    var Population = 14000000000;
    const response = await fetch(url);
    const data = await response.json();

    const statewise = data.statewise;
    const total = statewise.find(obj => obj.state == "Total");
    
    //Last Update Time
    const time = total.lastupdatedtime;
    const test = data.tested;

    //Active Cases Percentage
    active_cases_perc = (parseInt(total.active) / parseInt(total.confirmed)) * 100;

    //Cases Today
    var cases_today = parseInt(total.deltaconfirmed);

    //Deaths Today
    var deaths_today = total.deltadeaths;

    //Death Rate
    deaths_today_perc = (parseInt(total.deaths) / parseInt(total.confirmed)) * 100;

    //Total Tested
    var total_tested = parseInt(test[test.length - 1].totalsamplestested);

    //Vaccinations Cumulative
    vaccine = parseInt(test[test.length - 1].totalindividualsvaccinated);
    vaccine_perc = vaccine / 140000000;

    console.log(active_cases_perc);
    console.log(deaths_today_perc);
    console.log(vaccine_perc);
   
    //Updating HTML
    document.getElementById("date").innerHTML = time;
    
    document.getElementById("tested").innerHTML = total_tested;
    document.getElementById("cases").innerHTML = cases_today;

    document.getElementById("active_cases").innerHTML = parseInt(total.active);
    active_cases_perc = active_cases_perc.toFixed(2);
    document.getElementById("positivity").innerHTML = active_cases_perc + "%";

    document.getElementById("deaths").innerHTML = deaths_today;
    deaths_today_perc = deaths_today_perc.toFixed(2);
    document.getElementById("mortality").innerHTML = deaths_today_perc + "%";
   

    document.getElementById("vaccination_total").innerHTML = vaccine;
    vaccine_perc = vaccine_perc.toFixed(2);
    document.getElementById("vaccine_perc").innerHTML = vaccine_perc+"%";

    console.log(vaccine);

    callback();
}
getData(move);

function move() {
    var elem1 = document.getElementById("bar1");
    var elem2 = document.getElementById("bar2");
    var elem3 = document.getElementById("bar3");

    elem1.style.width = active_cases_perc + "%";
    elem2.style.width = deaths_today_perc + "%";
    elem3.style.width = vaccine_perc + "%";
}


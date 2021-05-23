const url = 'https://api.covid19india.org/data.json';
async function getData() {
    var Population = 1400000000;
    const response = await fetch(url);
    const data = await response.json();

    const statewise = data.statewise;
    const total = statewise.find(obj => obj.state == "Total");

    const test = data.tested;

    // var total_tested = 0;
    // test.map(test =>{
    //     if(test.totalindividualstested.length>0)
    //       total_tested+= parseInt(test.totalindividualstested)
    // })

    //Active Cases Percentage
    var active_cases_perc = (parseInt(total.active) / parseInt(total.confirmed)) * 100;
    console.log("Active Cases", total.active);
    console.log("Percentage:", active_cases_perc);

    //Cases Today
    var cases_today = parseInt(total.deltaconfirmed);
    console.log("Cases Today", total.deltaconfirmed);

    //Deaths Today
    var deaths_today = total.deltadeaths;
    console.log("Deaths Today", deaths_today);

    //Death Rate
    var deaths_today_perc = (parseInt(total.deaths) / parseInt(total.confirmed)) * 100;
    console.log("Death Rate", deaths_today_perc);

    //Total Tested
    var total_tested = parseInt(test[test.length - 1].totalsamplestested);
    console.log("tested", total_tested);

    //Vaccinations Cumulative
    var vaccine = parseInt(test[test.length - 1].totalindividualsvaccinated);
    console.log("Vaccinated", vaccine);

    //Vaccination Percentage
    console.log("Vaccination Percentage", vaccine / 140000000);
}
getData();

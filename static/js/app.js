function scroll(){
    window.scrollTo(0,100);
}


function showForm(){
    d3.select("#form").attr("class", "showForm");
    d3.select("#back").attr("class", "dont-show");
    d3.select("#reject").attr("class", "card dont-show")
    d3.select("#approve").attr("class", "card-deck dont-show");
    d3.select("#result").attr("class", "dont-show");
    window.scrollTo(0,0);
}

function sendJSON() {
    let fname = document.querySelector('#fname');
    let lname = document.querySelector('#lname');
    let gender = document.querySelector('#gender');
    let dep = document.querySelector('#dep');
    let graduate = document.querySelector('#graduate');
    let self = document.querySelector('#self');
    let loan = document.querySelector('#loan');
    let aincome = document.querySelector('#aincome');
    let cincome = document.querySelector('#cincome');
    let loanterm = document.querySelector('#loanterm');
    let parea = document.querySelector('#parea');
    let married = document.querySelector('#married');

    console.log(gender.value, dep.value, graduate.value, self.value, loan.value)
    // Converting JSON data to string 									
    var data = {
        "ApplicantIncome": aincome.value ? aincome.value : 0,
        "CoapplicantIncome": cincome.value.trim() ? cincome.value.trim() : 0,
        "LoanAmount": loan.value ? loan.value / 100 : 0,
        "Loan_Amount_Term": loanterm.value.trim() ? loanterm.value.trim() : 0,
        "Gender": gender.value.trim() === "Male" ? 1 : 0,
        "Married_Yes": married.value.trim() === "Married" ? 1 : 0,
        "Dependents_1": dep.value.trim() == 1 ? 1 : 0,
        "Dependents_2": dep.value.trim() == 2 ? 1 : 0,
        "Dependents_3+": dep.value.trim() > 2 ? 1 : 0,
        "Education_Not_Graduate": graduate.checked ? 0 : 1,
        "Self_Employed_Yes": self.checked ? 1 : 0,
        "Property_Area_Semiurban": parea.value.trim() == "Semi urban" ? 1 : 0,
        "Property_Area_Urban": parea.value.trim() == "Urban" ? 1 : 0
    };

    d3.json(
        "/", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }
    ).then(resp => showResult(resp));
}

function populateCards(data){
    d3.select("#result").html(
        "<p>Hey "+ fname.value + lname.value +"</p>"+"<br>"
        +"<p>The model predicted your loan will be approved" +"</p>")
    for(i=0;i<data["banks"].length;i++){
        d3.select("#cardImage"+(i+1)).attr("src",data["banks"][i]["image"])
        d3.select("#cardTitle"+(i+1)).html(data["banks"][i]["name"])
        d3.select("#cardInfo"+(i+1)).html(
        "<p> Loan Name:"+data["banks"][i]["loan"]+
        "</p><p>Rate:"+data["banks"][i]["fixed rate"]+"</p>")
    }
}

function showRecommendations(data){
    d3.select("#result").html(     
    "<p>Hey "+ fname.value + lname.value +"</p>"+"<br>"
    +"<p>The model predicted your loan will be rejected" +"</p>");
    d3.select("#recomendations").html(
        "<ul>"
        +"<li> Your income to be increased to: "+ data["income_updated"] +"</li>"
        +"<p> OR" +"<p>"
        +"<li> Your loan amount to be decreased to: "+data["loan_amount_updated"]+"</li>"
        +"<p> OR" +"</p>"
        +"<li> Your income to be increased to: "+data["income_linked"]+
        " and loan amount to be decreased to: "+data["loan_amount_linked"]+"</li>"+
        "</ul>"
        )
}

function showResult(data) {
    console.log("showResult");
    console.log(data);

    d3.select("#form").attr("class", "dont-show")
    d3.select("#back").attr("class", "show");
    if(data['pred'] == 1){
        populateCards(data)
        d3.select("#result").attr("class", "show green");
        d3.select("#reject").attr("class", "card dont-show")
        d3.select("#approve").attr("class", "card-deck show");
    }else{
        showRecommendations(data)
        d3.select("#result").attr("class", "show red");
        d3.select("#reject").attr("class", "card show")
        d3.select("#approve").attr("class", "card-deck dont-show");
    }

    window.scrollTo(0,document.body.scrollHeight);
}


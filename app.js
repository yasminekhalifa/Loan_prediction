function sendJSON(){ 
			
    let gender = document.querySelector('#gender'); 
    let dep = document.querySelector('#dep'); 
    let graduate = document.querySelector('#graduate'); 
    let self = document.querySelector('#self'); 
    let loan = document.querySelector('#loan'); 

    // Creating a XHR object 
    let xhr = new XMLHttpRequest(); 
    let url = "/predict"; 

    // open a connection 
    xhr.open("POST", url, true); 

    console.log(gender.value, dep.value, graduate.value, self.value, loan.value)
    // Converting JSON data to string 
    var data = JSON.stringify({ "gender": gender.value, "dep": dep.value, "graduate": graduate.value, "self": self.value, "loan": loan.value }); 
    console.log(data)
    // Sending data with the request 
    xhr.send(data); 
} 



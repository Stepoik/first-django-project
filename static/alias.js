// Блок с заходом людей в лобби
let game = false
let lobbyName = document.location.href
lobbyName = lobbyName.split('/')[lobbyName.split('/').length-1]
let ready = 'false'
let selfReady = 'false'
let numOfwords = 0
function getName(){  
	let name = prompt('Введите имя:')
	localStorage.setItem('name',name)
	return name
}
if (!localStorage.getItem('name')){
	let name = getName()
}else{
	let name = localStorage.getItem('name')
}
function changeName(){
	name = getName()
}
let team = 'spect'
let next = false
let alfList = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
let numList = ['1','2','3','4','5','6','7','8','9','0']
let alfNumList = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','1','2','3','4','5','6','7','8','9','0']

let root = false

let spectorTeam = document.querySelector('.spect')
let addTeam = document.querySelector('.addTeam')
let teamBoard = document.querySelector('.teamBoard')
function ClickTeam(teamno){
				team = teamno
}
function sortAllPlayers(respounse,players, teams){
	teams.push('spect')
	document.querySelectorAll('.team').forEach(teamno =>{
		if (teams.indexOf(teamno.className.split(' ')[1]) === -1 && ['addTeam','spect'].indexOf(teamno.className.split(' ')[1]) ===-1 ){
			$('.'+teamno.className.split(' ')[1]).remove()
		} 
	})
	teams.forEach(teamno =>{
		console.log(teamno)
		if (document.querySelector('.team.'+teamno)===null && teamno !== 'spect'){
			let newTeam = document.createElement('div')
			newTeam.className = 'team '+teamno
			newTeam.addEventListener('click', function(){
				team = teamno
			})
			teamBoard.appendChild(newTeam)
		}
	})
	document.querySelectorAll('.player').forEach(player => {
		if (player.className){
			if (players.indexOf(player.className.split(' ')[1]) === -1){
				$('.'+player.className.split(' ')[1]).remove()
				}
			}
		})
	players.forEach(player =>{
		let posOfPlayer = document.querySelector('.player.'+player)
		if (posOfPlayer ===null || (posOfPlayer.closest('.team').className.split(' ').indexOf(respounse[player][0]) === -1)||(posOfPlayer.textContent!==respounse[player][1])){
			$('.'+player).remove()
			let newPlayer = document.createElement('div')
			newPlayer.className = 'player '+player
			newPlayer.textContent = respounse[player][1]
			document.querySelector('.'+respounse[player][0]).appendChild(newPlayer)
		}
	})
}

spectorTeam.addEventListener('click', function(){
	team = 'spect'
})
addTeam.addEventListener('click', function(){
	if ($('.'+team).children().length > 1 || team === 'spect'){
		team = getSession()+'t'
	}
})


window.addEventListener('unload', delRequest)

function delRequest(){
	$.ajax({
		url:'/delContact/'+lobbyName
	})
}

let changeNamebtn = document.querySelector('.changeName')
changeNamebtn.addEventListener('click', changeName)

function getSession(){
	let session = ''
	session +=alfList[Math.floor(Math.random()*26)]
	for (i = 0; i < 5; i++){
		session+=alfNumList[Math.floor(Math.random()*36)]
	}
	return session
}

let session = getSession()
$.ajax({
	url:'/addcontact',
	data:{getInfo:true, url:lobbyName, session:session, team:team},
	async:false,
	success: function(data){
		console.log(data)
		if (data.session !== 'None'){
			if (data.root==='true'){
				root = true
				console.log(root)
			}
			session = data.session
			if (data.team!== ''){
			team = data.team}
			if (data.game === 'start'){
				team = 'spect'
			}
		}
	}
})
console.log(team)
console.log(root)
if (root === true){
	let startbutton = document.createElement('button')
	startbutton.className = 'start'
	startbutton.textContent = 'Start game'
	document.querySelector('body').appendChild(startbutton)
	document.querySelector('.start').addEventListener('click', gameStart)
}

//конец блока лобби
function requestPlayer(){
	console.log(game)
	if (!game){
		$.ajax({
		data:{url:lobbyName, name:name,root:root, team:team, session:session},
		url:'/addcontact',
		success: function(respounse){
			let teams = []
			let players = []
			for (inf in respounse){
				if (respounse[inf] === 'team'){
					teams.push(inf)
				}else if (['game', 'ready'].indexOf(inf) ===-1){
					players.push(inf)
				}
			}
			if (respounse.game === 'true'){
				game = true
			}
			// ready = respounse.ready
			console.log(players, teams)
			sortAllPlayers(respounse, players, teams)
		}
	})
	}else if (ready === 'false'){
		$.ajax({
			data:{lobby:lobbyName,selfReady:selfReady},
			url:'/gameStart',
			success: function(respounse){
				ready = respounse.ready
				let questPl = respounse.questor
				let answPl = respounse.answer
				gameReadyCheck(questPl, answPl)
			}
		})
	}else{
		$.ajax({
			data:{lobby:lobbyName, next:next},
			url:'/gameGo',
			success: function(respounse){
				next = false
				let time = respounse.time
				let words = respounse.words
				let questor = respounse.questor
				gameGo(time, words)
			},
			async:false
		})
	}
}

setInterval(requestPlayer, 100)
//Блок игры
function gameStart(){
	game = true
	$('.start').remove()
	document.querySelectorAll('.team').forEach(teams =>{
		if (['addTeam', 'spect'].indexOf(teams.className.split(' ')[1]) == -1){
			teams.removeEventListener('click', ClickTeam())
		}
	})
}

function gameReadyCheck(questPl, answPl){
	$('.addTeam').remove()
	if (ready === 'true'){
		$('.ready').remove()
		$('.next').remove()
		$('.timer').remove()
		if (questPl === session){
			let nextbutton = document.createElement('div')
			nextbutton.className = 'button next'
			nextbutton.textContent = 'Next'
			nextbutton.addEventListener('click', function(){
				next = true
				document.querySelector('.next').scrollIntoView()
			})
			let timer = document.createElement('div')
			timer.className = 'timer'
			document.querySelectorAll('.content')[1].insertBefore(timer, document.querySelectorAll('.content')[1].firstChild)
			document.querySelector('.buttons').appendChild(nextbutton)
		}
		return 'end'
	}
	if ((questPl === session || answPl === session)&&(document.querySelector('.ready') === null)){
		if (document.querySelector('.ready') === null){
		let readybtn = document.createElement('div')
			readybtn.className = 'button ready'
			readybtn.textContent = 'Ready'
			readybtn.addEventListener('click', function(){
				if (selfReady === 'true'){
					selfReady = 'false'
				}else{
					selfReady = 'true'
				}
			})
			document.querySelector('.buttons').appendChild(readybtn)
		}
	}
}
function gameGo(time, words){
	if (document.querySelector('.timer')){
		timer = time
		if (time < 10){
			timer = '0'+time
		}
	document.querySelector('.timer').textContent = '00:'+timer}
	if (time === 0){
		$('.timer').remove()
		$('.next').remove()
	}
	for (i = words.length - document.querySelectorAll('.word').length; i> 0;i-- ){
		newWord = document.createElement('div')
		newWord.className = 'word'
		newWord.textContent = words[words.length-i]
		document.querySelector('.buttons').insertBefore(newWord, document.querySelector('.buttons').lastChild)
	}
}


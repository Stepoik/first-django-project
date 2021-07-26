let lobby = document.location.href.split('/')[document.location.href.split('/').length-1]
close = 'false'
wordsPress = 'false'
function getInfo(async = true){$.ajax({
	data:{name:name, close:close},
	url:'getInfo/'+lobby,
	success:function(data){
		start = data.start
		session = data.session
		players = data.players
		teams = data.teams
		ready = data.ready
		root = data.root
		if (start === 'true'){
			questor = data.questor
			words = data.words
			answer = data.answer
		}
		if (ready === 'true'){
			timer = data.timer
			if (timer <= 0){
				wordsPress = data.wordspress
			}
		}
	},
	async:async
})
}
function send(){
	$.ajax({
		url:'send/'+lobby,
		async:false
	})
}
function changeName(){
	name = prompt('Введите имя')
}
function startGame(){
	console.log('start')
	$.ajax({
		method:'get',
		url:'startGame/'+lobby,
	})
}
function createTeam(){
	console.log('create')
	$.ajax({
		url:'createTeam/'+lobby,
		method:'get',
	})
}
function changeTeam(team){
	console.log('change')
	$.ajax({
		data:{team:team},
		method:'get',
		url:'changeTeam/'+lobby
	})
}
function delPlayer(){
	$.ajax({
		url:'delplayer/'+lobby
	})
}
function getReady(){
	$.ajax({
		url:'ready/'+lobby
	})
}
function nextWord(){
	$.ajax({
		url:'next/'+lobby
	})
}
function changeWordStatus(word){
	$.ajax({
		data:{word:word},
		url:'changeStatus/'+lobby
	})
}
document.querySelector('.changeName').addEventListener('click', function(){changeName()})
document.querySelector('.spect').addEventListener('click', function(){changeTeam('spect')})
getInfo(false)
if (start === 'false'){
	addTeambtn = document.createElement('div')
	addTeambtn.className = 'team addTeambtn'
	addTeambtn.textContent = 'Add team'
	addTeambtn.addEventListener('click', createTeam)
	document.querySelector('.teamBoard').appendChild(addTeambtn)
}
function drawlobby(){
	if (root === 'true' && document.querySelectorAll('.team').length > 2 && start === 'false' && document.querySelector('.start') === null){
		let startbtn = document.createElement('div')
		startbtn.className = 'button start'
		startbtn.textContent = 'Start'
		startbtn.addEventListener('click', function(){
			startGame()
		})
		document.querySelector('.buttons').appendChild(startbtn)
	}else if (document.querySelectorAll('.team').length <= 2 || start !== 'false' ){
		$('.start').remove()
	}
	teams.forEach(team => {
		if (document.querySelector('.team.'+team) === null){
			let newTeam = document.createElement('div')
			newTeam.className = 'team '+team
			newTeam.addEventListener('click', function(){changeTeam(team)})
			document.querySelector('.teamBoard').appendChild(newTeam)
		}
	})
	document.querySelectorAll('.team').forEach(team =>{
		if (['addTeambtn','spect'].indexOf(team.className.split(' ')[1]) === -1 && teams.indexOf(team.className.split(' ')[1]) === -1){
			$('.'+team.className.split(' ')[1]).remove()
		}
	})
	players.forEach(player =>{
		if (document.querySelector('.'+player[2]) === null){
			let newPlayer = document.createElement('div')
			newPlayer.className = 'player '+player[2]
			newPlayer.textContent = player[0]
			document.querySelector('.'+player[1]).appendChild(newPlayer)
		}else if(document.querySelector('.'+player[2]).closest('.team').className.split(' ')[1] !== player[1]){
			$('.'+player[2]).remove()
			let newPlayer = document.createElement('div')
			newPlayer.className = 'player '+player[2]
			newPlayer.textContent = player[0]
			document.querySelector('.'+player[1]).appendChild(newPlayer)
		}else if(document.querySelector('.'+player[2]).textContent !== player[0]){
			document.querySelector('.'+player[2]).textContent = player[0]
		}
	})
	document.querySelectorAll('.player').forEach(player =>{
		for (pla in players){
			if (players[pla][2] === player.className.split(' ')[1]){
				break
			}
			if (parseInt(pla) === players.length-1){
				$('.'+player.className.split(' ')[1]).remove()
			}
		}
	})
	if (start === 'true'){
		if (answer[1] === 'true'){
			answerColor = '#7CE17B'
		}else{
			answerColor = '#A5E1DA'
		}
		if (questor[1] === 'true'){
			questorColor = '#3CE100'
		}else{
			questorColor = '#7ED4E1'
		}
		if(ready === 'true'){
			questorColor = '#FFFFFF'
			answerColor = '#FFFFFF'
		}
		document.querySelector('.'+answer[0]).style.background = answerColor
		document.querySelector('.'+questor[0]).style.background= questorColor
		if ((questor[2] === 'true' || answer[2] === 'true')&&(ready === 'false')){
			if (document.querySelector('.ready') === null){
				let readybtn = document.createElement('div')
				readybtn.className = 'button ready'
				readybtn.textContent = 'Ready'
				readybtn.addEventListener('click', function(){getReady()})
				document.querySelector('.buttons').appendChild(readybtn)
			}
		}
	}
	if (ready === 'true'){
		$('.ready').remove()
		if (document.querySelector('.words') === null){
			let wordsDiv = document.createElement('div')
			wordsDiv.className = 'words'
			let timerDiv = document.createElement('div')
			timerDiv.className = 'timer'
			wordsDiv.appendChild(timerDiv)
			document.querySelector('.Allcontent').insertBefore(wordsDiv,document.querySelector('.buttons'))
		}
		if (questor[2] === 'true'){
			if (document.querySelector('.next') === null){
				let nextbutton = document.createElement('div')
				nextbutton.className = 'button next'
				nextbutton.textContent = 'Next'
				nextbutton.addEventListener('click', function(){
					nextWord()
					nextbutton.scrollIntoView()
				})
				document.querySelector('.buttons').appendChild(nextbutton)
			}
		}
		if (timer > 0){
			if (timer<10){
				document.querySelector('.timer').textContent = '00:0'+timer
			}else{
				document.querySelector('.timer').textContent = '00:'+timer
			}
		}
		words.forEach(word=>{
			if (document.querySelector('.'+word[0]) === null){
				let newWord = document.createElement('div')
				newWord.className = word[0]
				newWord.textContent = word[0]
				document.querySelector('.words').append(newWord)
			}
			if (wordsPress === 'true' && document.querySelector('.'+word[0]).className.split(' ').length === 1){
				document.querySelector('.'+word[0]).className +=' endround'
				document.querySelector('.'+word[0]).addEventListener('click', function(){
					changeWordStatus(word[0])
				})
			}
			if (word[1] === 'true'){
				document.querySelector('.'+word[0]).style.background = '#A5E1DA'
			}else{
				document.querySelector('.'+word[0]).style.background = '#FFFFFF'
			}
		})
		if (timer <=0){
			if ((questor[2] === 'true' || answer[2] === 'true') && document.querySelector('.send') === null){
				let sendbtn = document.createElement('div')
				sendbtn.className = 'button send'
				sendbtn.textContent = 'Send'
				sendbtn.addEventListener('click', function(){
					send()
				})
				document.querySelector('.buttons').appendChild(sendbtn)
			}
			$('.timer').remove()
			$('.next').remove()
		}
	}else{
		$('.send').remove()
		$('.words').remove()
	}
}
timer = setInterval(function(){
	getInfo()
	if (start === 'true'){
		$('.addTeambtn').remove()
	}
	drawlobby()
},100)
this.addEventListener('unload', function(){
	close = 'true'
	delPlayer()
})
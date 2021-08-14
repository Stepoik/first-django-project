(function(){
	const lobby = window.location.href.split('/')[window.location.href.split('/').length-2]
	const userSocket = new WebSocket(
		'ws://'
	            + window.location.host
	            + '/ws/bunker/'
	            + lobby
	            +'/')
	const checkready = setInterval(function(){
	if (userSocket.readyState === 1){
		userName = prompt('Your name')
		console.log('send')
		userSocket.send(JSON.stringify({
		'function':'GetPlayers',
		'name':userName
		}))
		clearInterval(checkready)
	}})
	userSocket.onmessage = function(e){
		let data = JSON.parse(e.data)
		if (data.function === 'GetPlayers') {
			getPlayers(data)
		}else if (data.function === 'changeTeam'){
			changeTeam(data)
		}else if(data.function === 'addPlayer'){
			addPlayer(data)
		}else if (data.function === 'delPlayer'){
			$('.'+data.id).remove()
		}else if (data.function === 'getspecif'){
			drawSpec(data)
		}else if (data.function === 'open'){
			open(data)
		}
	}
	function getPlayers(data){
		data.players.forEach(player =>{
			addPlayer(player)
		})
		if (data.root === 'true'){
			startbtn = document.createElement('div')
			startbtn.className = 'start'
			startbtn.textContent = 'start'
			startbtn.addEventListener('click', function(){
				userSocket.send(JSON.stringify({
					'function':'start'
				}))
			})
			document.querySelector('.buttons').appendChild(startbtn)
		}
	}
	function addPlayer(player){
		let playerDiv = document.createElement('div')
		playerDiv.className = 'player '+player.id
		playerDiv.textContent = player.name
		if (player.play === 'true'){
			document.querySelector('.players').appendChild(playerDiv)
		}else{
			playerDiv.className = player.id
			document.querySelector('.spectors').appendChild(playerDiv)
		}
	}
	function changeTeam(player){
		console.log('change')
		let playerDiv = document.createElement('div')
		playerDiv.className = 'player '+player.id
		playerDiv.textContent = document.querySelector('.'+player.id).textContent
		$('.'+player.id).remove()
		if (player.play === 'true'){
			document.querySelector('.players').appendChild(playerDiv)
		}else{
			document.querySelector('.spectors').appendChild(playerDiv)
		}
	}
	function drawSpec(spec){
		for (special in spec){
			if (special != 'function'){
				let selfspec = document.createElement('div')
				selfspec.className = 'self '+ special
				selfspec.textContent = spec[special]
				selfspec.addEventListener('click', function(){
					userSocket.send(JSON.stringify({
						'function':'open',
						'spec':selfspec.className.split(' ')[1]
					}))
				})
				document.querySelector('.specific').appendChild(selfspec)
			}
		}
	}
	function open(data){
		let spec = document.createElement('div')
		spec.className = 'spec'
		spec.textContent = data.spec
		document.querySelector('.'+data.id).appendChild(spec)
	}
	const join = document.querySelector('.joinbtn')
	join.addEventListener('click', function(){
		userSocket.send(JSON.stringify({
			'function':'changeTeam',
			'play':'true'
		}))
	})
	document.querySelector('.spectors').addEventListener('click', function(){
		userSocket.send(JSON.stringify({
			'function':'changeTeam',
			'play':'false'
		}))})
})();
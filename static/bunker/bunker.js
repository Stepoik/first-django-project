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
		$.ajax({
			url:'getplayers',
			success:function(data){
				getPlayers(data)
			}
		})
		clearInterval(checkready)
	}})
	userSocket.onmessage = function(e){
		let data = JSON.parse(e.data)
		if (data.function === 'add_player'){
			addPlayer(data)
		}else if (data.function === 'change'){
			document.querySelector('.'+data.id).remove()
			addPlayer(data)
		}else if (data.function === 'delete'){
			$('.'+data.id).remove()
		}else if (data.function === 'get_spec'){
			$('.joinbtn').remove()
			draw_self_spec(data)
			draw_bunker(data)
		}else if (data.function === 'open'){
			open(data)
		}else if (data.function === 'kick'){
			console.log(data.player)
			$('.'+data.player).remove()
		}
	}
	document.querySelector('.spectors').addEventListener('click', function(){
		userSocket.send(JSON.stringify({
			'change':false
		}))
	})
	function getPlayers(data){
		root = data.root
		data.players.forEach(player=>{
			addPlayer(player)
		})
		data.all_specs.forEach(spec =>{
			open(spec)
		})
		draw_self_spec(data)
		if (data.inlobby === false){
			let userName = prompt('Ваш ник?')
			userSocket.send(JSON.stringify({
				'new_player':userName,
				'root':data.root,
				'session':data.session
			}))
		}else{
			userSocket.send(JSON.stringify({
				'new_player':'None',
				'online':true,
				'session':data.session
			}))
		}
		if (data.start === false){
			let join = document.createElement('div')
			join.className = 'joinbtn'
			join.textContent = 'Войти'
			join.addEventListener('click', function(){
								userSocket.send(JSON.stringify({
									'change':true
								}))})
			document.querySelector('.buttons').appendChild(join)
		}else{
			draw_bunker(data)
		}
		if (data.root && data.start === false){
			let startbtn = document.createElement('div')
			startbtn.className = 'button start'
			startbtn.textContent = 'start'
			startbtn.addEventListener('click', function(){
				userSocket.send(JSON.stringify({
					'function':'start'
				}))})
			document.querySelector('.buttons').appendChild(startbtn)
		}
	}
	function addPlayer(player){
		let plDiv = document.createElement('div')
		plDiv.className = player.id
		plDiv.textContent = player.name
		if (player.play === true){
			plDiv.className +=' player'
			document.querySelector('.players').appendChild(plDiv)
		}else{
			document.querySelector('.spectors').appendChild(plDiv)
		}
		if (player.specs){
			console.log(player.specs)
			for (spec in player.specs){
				open(player.specs[spec])
			}
		}
		if (root){
			console.log('root')
			document.querySelector('.'+player.id+'.player').onmouseenter = function(){
				console.log(player.id)
				let kickbtn = document.createElement('div')
				kickbtn.className = player.id+' kick button'
				kickbtn.textContent = '×'
				kickbtn.addEventListener('click',function(){
					userSocket.send(JSON.stringify({
						'kick':player.id
					}))
				})
				document.querySelector('.'+player.id).appendChild(kickbtn)
			}
			document.querySelector('.'+player.id+'.player').onmouseleave = function(){
				console.log('loalsdas')
				$('.'+player.id+'.kick.button').remove()
			}
		}
	}
	function draw_self_spec(data){
		$('.start').remove()
		for (spec in data.self_specs){
			console.log(spec)
			let new_spec = document.createElement('div')
			new_spec.className = 'self '+spec
			new_spec.textContent = data.self_specs[spec]
			new_spec.addEventListener('click', function(){
				userSocket.send(JSON.stringify({
					'open':new_spec.className.split(' ')[1]
				}))
			})
			document.querySelector('.specific').appendChild(new_spec)
		}
	}
	function open(spec){
		console.log(spec)
		let new_spec = document.createElement('div')
		new_spec.className = 'spec'
		new_spec.textContent = spec.spec
		document.querySelector('.'+spec.player).appendChild(new_spec)
	}
	function draw_bunker(data){
		console.log(data.bunker)
		let bunker = document.createElement('div')
		bunker.className = 'bunker'
		bunker.textContent = 'Бункер: '
		for (cond in data.bunker){
			let divcond = document.createElement('div')
			divcond.className = 'bunkercond '+cond
			divcond.textContent = data.bunker[cond]
			bunker.appendChild(divcond)
		}
		document.querySelector('.content').insertBefore( bunker,document.querySelector('.content').firstChild)
	}
})()
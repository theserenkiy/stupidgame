
class Popup
{
	shown = 0
	busy = 0
	timeout = null
	showqueue_num = 0

	constructor(el_selector, p={})
	{
		this.el = document.querySelector(el_selector)
		this.transition_ms = p.transition_ms || 300
		this.display = p.display || 'flex'
		this.fadeout_ms = p.fadeout_ms || 0

	}

	remClass(name)
	{
		remClass(this.el,name)
	}

	async waitBusy()
	{
		while(this.busy)
		{
			await new Promise(s => setTimeout(s,50));
		}
	}

	async show(html,class_before='',style_before=null)
	{
		let qnum = ++this.showqueue_num;
		cl('show '+qnum)
		if(this.shown)
		{
			cl('shown -> hide')
			await this.hide()
		}
		await this.waitBusy()

		if(qnum != this.showqueue_num)
			return

		this.busy = 1
		
		if(class_before)
			this.el.className += ' '+class_before

		if(style_before)
		{
			for(let i in style_before)
				this.el.style[i] = style_before[i]
		}

		if(typeof html == 'string')
			this.el.innerHTML = html
		else
		{
			this.el.innerHTML = ''
			this.el.appendChild(html)
		}
		this.el.style.display = this.display

		await delay(50)

		this.el.className += ' shown'
		this.shown = 1
		this.busy = 0

		await delay(this.transition_ms)

		if(qnum != this.showqueue_num)
			return

		if(this.fadeout_ms)
			this.fadeout(qnum)
	}

	async fadeout(qnum)
	{
		cl("fadeout")
		this.el.className += ' fadeout_transition'
		await delay(50)
		this.remClass('shown')
		await delay(this.fadeout_ms)
		if(qnum != this.showqueue_num)
			return
		this.hide(['fadeout_transition'])
	}

	async hide(rem_classes=[])
	{
		//cl('try hide')
		if(!this.shown && !this.busy)
			return
		//cl('hide, wait busy')
		await this.waitBusy()
		//cl('ok')
		if(!this.shown)
			return
		//cl('do hide')
		this.busy = 1;
		this.remClass('shown')

		//cl('await transition '+this.transition_ms)
		await delay(this.transition_ms)
		rem_classes.push('fadeout_transition')
		for(let cls of rem_classes)
			this.remClass(cls)

		this.el.style.display = 'none'
		this.shown = 0
		this.busy = 0
	}
}
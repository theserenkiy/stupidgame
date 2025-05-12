
class Popup
{
	shown = 0
	busy = 0
	timeout = null

	constructor(el_selector,transition_ms=300,display='flex',fadeout_ms=0)
	{
		this.el = document.querySelector(el_selector)
		this.transition = transition_ms
		this.display = display
		this.fadeout_ms = fadeout_ms
		cl({el_selector, fadeout_ms})
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
		if(this.shown)
		{
			cl('shown')
			await this.hide()
		}
		await this.waitBusy()

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

		if(this.fadeout_ms)
			this.fadeout()
	}

	async fadeout()
	{
		cl("fadeout")
		this.el.className += ' fadeout_transition'
		this.remClass('shown')
		await delay(this.fadeout_ms)
		this.hide(['fadeout_transition'])
	}

	async hide(rem_classes=[])
	{
		if(!this.shown && !this.busy)
			return
		cl('hide')
		await this.waitBusy()
		if(!this.shown)
			return
		this.busy = 1;
		this.remClass('shown')
		await delay(this.transition)
		for(let cls of rem_classes)
			this.remClass(cls)

		this.el.style.display = 'none'
		this.shown = 0
		this.busy = 0
	}
}
/*======================================
Evalio Evaluation Controller
======================================*/

const Evaluation = {

    /*==================================
    Cache
    ==================================*/

    cache:{},

    /*==================================
    State
    ==================================*/

    state:{

        knowledge:null,

        activeCategory:null,

        answers:{},

        completed:0,

        reviewedCategories:new Set()

        ,

        flowLines:[]

    },

    /*==================================
    Initialize
    ==================================*/

    async init(){

        this.cacheElements();

        this.bindEvents();

        await this.loadKnowledge();

        this.renderCategories();

        this.initializeAnswers();

        this.updateProgress();

        this.setupCanvas();

    },

    /*==================================
    Cache DOM
    ==================================*/

    cacheElements(){

        this.cache.accordionContainer=

            document.getElementById(

                "accordion-container"

            );

        this.cache.progressPercent=

            document.getElementById(

                "progress-percent"

            );

        this.cache.progressRing=

            document.querySelector(

                ".ring-value"

            );

        this.cache.evaluateButton=

            document.getElementById(

                "evaluate-button"

            );

        this.cache.backButton=

            document.getElementById(

                "back-button"

            );

        this.cache.canvas=

            document.getElementById(

                "wave-canvas"

            );

    },

    /*==================================
    Events
    ==================================*/

    bindEvents(){

        this.cache.backButton
        ?.addEventListener(
            "click",
            ()=>window.location.href="index.html"
        );

        this.cache.evaluateButton
        ?.addEventListener(
            "click",
            ()=>this.submitEvaluation()
        );

        this.cache.accordionContainer
        ?.addEventListener(
            "click",
            (event)=>this.handleAccordion(event)
        );

        this.cache.accordionContainer
        ?.addEventListener(

            "change",

            (event)=>this.handleFact(event)

        );

        window.addEventListener(

            "resize",

            ()=>{

                this.resizeCanvas();

                this.createFlowLines();

            }

        );

    },

    /*==================================
    Load Knowledge
    ==================================*/

    async loadKnowledge(){

        try{

            /*
            Temporary Source

            Later:
            /api/v1/knowledge
            */

            const response=

                await fetch(

                    "data/knowledge.json"

                );

            if(!response.ok){

                throw new Error(

                    "Failed to load knowledge."

                );

            }

            this.state.knowledge=

                await response.json();

            console.log(

                "Knowledge Loaded",

                this.state.knowledge

            );

        }

        catch(error){

            console.error(

                error

            );

        }

    },

    /*==================================
    Render Categories
    ==================================*/

    renderCategories(){

        if(!this.state.knowledge) return;

        this.cache.accordionContainer.innerHTML="";

        this.state.knowledge.categories.forEach(

            (category,index)=>{

                this.cache.accordionContainer.insertAdjacentHTML(

                    "beforeend",

                    this.createAccordion(

                        category,

                        index

                    )

                );

            }

        );

        lucide.createIcons();

    },

    /*==================================
    Create Accordion
    ==================================*/

    createAccordion(category,index){

        return `

        <article
            class="accordion-item ${index===0?"active":""}"
            data-category="${category.id}"
        >

            <button class="accordion-header">

                <div class="accordion-left">

                    <div class="accordion-icon">

                        <i data-lucide="${category.icon}"></i>

                    </div>

                    <div class="accordion-title">

                        <h3>

                            ${index+1}. ${category.name}

                        </h3>

                        <p>

                            ${category.description}

                        </p>

                    </div>

                </div>

                <div class="accordion-right">

                    <span class="selected-count">

                        0 / ${category.facts.length} dipilih

                    </span>

                    <i
                        class="accordion-arrow"
                        data-lucide="chevron-down"
                    ></i>

                </div>

            </button>

            <div class="accordion-body">

                <div class="checklist-grid">

                    ${category.facts.map(

                        fact=>this.createFactCard(fact)

                    ).join("")}

                </div>

            </div>

        </article>

        `;

    },

    /*==================================
    Handle Accordion
    ==================================*/

    handleAccordion(event){

        const header =
            event.target.closest(
                ".accordion-header"
            );

        if(!header) return;

        const accordion =
            header.closest(
                ".accordion-item"
            );

        const categoryId =
            accordion.dataset.category;

        if(categoryId===this.state.activeCategory){

            return;

        }

        this.toggleAccordion(categoryId);

    },

    /*==================================
    Create Fact Card
    ==================================*/

    createFactCard(fact){

        return `

        <label
            class="check-card"
            data-fact="${fact.id}"
        >

            <input
                type="checkbox"
                class="fact-checkbox"
            >

            <span
                class="checkbox"
            ></span>

            <div class="check-info">

                <h4>

                    ${fact.question}

                </h4>

                <p>

                    ${fact.description}

                </p>

            </div>

        </label>

        `;

    },

    /*==================================
    Handle Fact
    ==================================*/

    handleFact(event){

        const input = event.target;

        if(!input.matches(".fact-checkbox")) return;

        const card =
            input.closest(".check-card");

        const accordion =
            input.closest(".accordion-item");

        const categoryId =
            accordion.dataset.category;

        const factId =
            card.dataset.fact;

        this.toggleFact(

            categoryId,

            factId,

            input.checked,

            card

        );

    },

    /*==================================
    Toggle Fact
    ==================================*/

    toggleFact(

        categoryId,

        factId,

        checked,

        card

    ){

        this.state.answers[categoryId][factId] = checked;

        this.state.reviewedCategories.add(
            categoryId
        );

        // Sinkronkan tampilan card
        this.syncFactCard(

            card,

            checked

        );

        // Update counter kategori
        this.updateCategoryCounter(

            categoryId

        );

        // Update progress keseluruhan
        this.updateProgress();

    },

    /*==================================
    Sync Fact Card
    ==================================*/

    syncFactCard(

        card,

        checked

    ){

        card.classList.toggle(

            "selected",

            checked

        );

    },

    /*==================================
    Toggle Accordion
    ==================================*/

    toggleAccordion(categoryId){

        document
        .querySelectorAll(".accordion-item")
        .forEach(

            item=>{

                item.classList.remove("active");

            }

        );

        const current =
            this.cache.accordionContainer
            .querySelector(

                `[data-category="${categoryId}"]`

            );

        current.classList.add("active");

        this.state.activeCategory =
            categoryId;

        this.state.reviewedCategories.add(
            categoryId
        );

        this.updateProgress();

    },

    /*==================================
    Initialize Category Answers
    ==================================*/

    initializeAnswers(){

        this.state.knowledge.categories.forEach(

            category=>{

                this.state.answers[category.id]={};

                category.facts.forEach(

                    fact=>{

                        this.state.answers[category.id][fact.id]=false;

                    }

                );

            }

        );

    },

    /*==================================
    Category Counter
    ==================================*/

    updateCategoryCounter(

        categoryId

    ){

        const category=

            this.state.knowledge.categories.find(

                item=>

                    item.id===categoryId

            );

        const answers=

            this.state.answers

            [categoryId];

        const selected=

            Object.values(

                answers

            ).filter(Boolean).length;

        const counter=

            this.cache.accordionContainer

            .querySelector(

                `[data-category="${categoryId}"] .selected-count`

            );

        counter.textContent=

            `${selected} / ${category.facts.length} dipilih`;

    },

   /*==================================
    Progress
    ==================================*/

    updateProgress(){

        let selectedFacts = 0;

        let totalFacts = 0;

        this.state.knowledge.categories.forEach(

            category=>{

                const answers=

                    this.state.answers[category.id];

                const selected=

                    Object.values(

                        answers

                    ).filter(Boolean).length;

                selectedFacts+=selected;

                totalFacts+=category.facts.length;

            }

        );

        this.state.completed=
            this.state.reviewedCategories.size;

        const percent=

            Math.round(

                selectedFacts/

                totalFacts

                *100

            );

        this.cache.progressPercent.textContent=

            `${percent}%`;

        this.updateProgressRing(percent);

        this.updateCategoryProgress();

        this.updateTimeline();

        this.updateButton();

    },

    /*==================================
    Category Progress
    ==================================*/

    updateCategoryProgress(){

        const progressText=

            document.querySelector(

                ".progress-center span"

            );

        progressText.textContent=

            `${this.state.completed} / ${this.state.knowledge.categories.length} Kategori`;

    },

    /*==================================
    Progress Ring
    ==================================*/

    updateProgressRing(percent){

        const circle=

            this.cache.progressRing;

        const radius=70;

        const circumference=

            2*Math.PI*radius;

        circle.style.strokeDasharray=

            circumference;

        circle.style.strokeDashoffset=

            circumference-

            (percent/100)*circumference;

    },

    /*==================================
    Timeline
    ==================================*/

    updateTimeline(){

        const items=

            document.querySelectorAll(

                ".timeline-item"

            );

        items.forEach(

            item=>item.classList.remove(

                "active"

            )

        );

        if(this.state.completed===0){

            items[0].classList.add(

                "active"

            );

        }

        else if(

            this.state.completed<

            this.state.knowledge.categories.length

        ){

            items[1].classList.add(

                "active"

            );

        }

        else{

            items[2].classList.add(

                "active"

            );

        }

    },

    /*==================================
    Submit Evaluation
    ==================================*/

    async submitEvaluation(){

        if(!this.validate()){

            return;

        }

        const payload=

            this.buildPayload();

        this.cache.evaluateButton.disabled=true;

        this.cache.evaluateButton
            .querySelector("span")
            .textContent="Mengevaluasi...";

        try{

            const response=await fetch(
                "http://127.0.0.1:8000/evaluation",
                {
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json"
                    },
                    body:JSON.stringify(payload)
                }
            );

            const result=await response.json();

            if(!response.ok || result.success===false){

                throw new Error(
                    result.message ||
                    "Evaluation failed."
                );

            }

            localStorage.setItem(
                "evalioEvaluationResult",
                JSON.stringify({
                    request:payload,
                    response:result,
                    evaluatedAt:new Date().toISOString()
                })
            );

            window.location.href="result.html";

        }

        catch(error){

            console.error(error);

            alert(
                "Evaluasi gagal. Pastikan backend API berjalan di http://127.0.0.1:8000."
            );

            this.cache.evaluateButton.disabled=false;

            this.cache.evaluateButton
                .querySelector("span")
                .textContent="Evaluasi Sekarang";

        }

    },

    /*==================================
    Validate
    ==================================*/

    validate(){

        const payload=this.buildPayload();

        if(payload.facts.length===0){

            alert(

                "Pilih minimal satu fakta yang sesuai dengan event Anda."

            );

            return false;

        }

        return true;

    },

    /*==================================
    Build Payload
    ==================================*/

    buildPayload(){

        const facts=[];

        Object.values(

            this.state.answers

        ).forEach(

            category=>{

                Object.entries(

                    category

                ).forEach(

                    ([fact,value])=>{

                        if(value){

                            facts.push(fact);

                        }

                    }

                );

            }

        );

        return{

            facts

        };

    },

    /*==================================
    Background Canvas
    ==================================*/

    setupCanvas(){

        if(!this.cache.canvas) return;

        this.cache.context=

            this.cache.canvas.getContext("2d");

        this.resizeCanvas();

        this.createFlowLines();

        this.animateCanvas();

    },

    resizeCanvas(){

        if(!this.cache.canvas) return;

        this.cache.canvas.width=window.innerWidth;

        this.cache.canvas.height=window.innerHeight;

    },

    createFlowLines(){

        if(!this.cache.canvas) return;

        this.state.flowLines=[];

        const count=34;

        const startY=this.cache.canvas.height*.12;

        for(let i=0;i<count;i++){

            this.state.flowLines.push({

                y:startY+i*6,

                speed:.22+Math.random()*.18,

                opacity:.045+Math.random()*.055,

                width:.7+Math.random()*1.2,

                phase:Math.random()*Math.PI*2,

                amplitude:18+Math.random()*40

            });

        }

    },

    animateCanvas(){

        const canvas=this.cache.canvas;

        const context=this.cache.context;

        if(!canvas || !context) return;

        context.clearRect(0,0,canvas.width,canvas.height);

        this.state.flowLines.forEach(

            line=>{

                line.phase+=line.speed*.01;

                const gradient=context.createLinearGradient(

                    0,

                    line.y,

                    canvas.width,

                    line.y

                );

                gradient.addColorStop(0,"rgba(255,111,0,0)");
                gradient.addColorStop(.20,`rgba(255,137,0,${line.opacity})`);
                gradient.addColorStop(.52,`rgba(255,218,44,${line.opacity*2})`);
                gradient.addColorStop(.82,`rgba(255,122,0,${line.opacity})`);
                gradient.addColorStop(1,"rgba(255,111,0,0)");

                context.beginPath();

                context.lineWidth=line.width;

                context.strokeStyle=gradient;

                for(let x=0;x<=canvas.width;x+=8){

                    const y=

                        line.y+

                        Math.sin((x/canvas.width)*Math.PI*3.1+line.phase)*

                        line.amplitude+

                        Math.sin((x/canvas.width)*Math.PI*7.2+line.phase*.8)*

                        10;

                    if(x===0){

                        context.moveTo(x,y);

                    }

                    else{

                        context.lineTo(x,y);

                    }

                }

                context.stroke();

            }

        );

        requestAnimationFrame(

            ()=>this.animateCanvas()

        );

    }

};


/*======================================
Application Start
======================================*/

document.addEventListener(

    "DOMContentLoaded",

    ()=>Evaluation.init()

);

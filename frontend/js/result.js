"use strict";

const ResultPage = {

    cache:{},

    state:{
        knowledge:null,
        stored:null,
        result:null,
        flowLines:[],
        animationId:null
    },

    async init(){
        this.cacheElements();
        this.bindEvents();
        await this.loadKnowledge();
        this.state.stored=this.readStoredEvaluation();
        this.state.result=this.buildResult();
        this.render();
        this.setupCanvas();
        lucide.createIcons();
    },

    cacheElements(){
        this.cache.canvas=document.getElementById("wave-canvas");
        this.cache.scoreRing=document.getElementById("score-ring");
        this.cache.scorePercent=document.getElementById("score-percent");
        this.cache.decisionTitle=document.getElementById("decision-title");
        this.cache.decisionSubtitle=document.getElementById("decision-subtitle");
        this.cache.decisionDescription=document.getElementById("decision-description");
        this.cache.statusIcon=document.getElementById("status-icon");
        this.cache.riskPill=document.getElementById("risk-pill");
        this.cache.factsScore=document.getElementById("facts-score");
        this.cache.factsPercent=document.getElementById("facts-percent");
        this.cache.categoriesScore=document.getElementById("categories-score");
        this.cache.categoriesPercent=document.getElementById("categories-percent");
        this.cache.riskLevel=document.getElementById("risk-level");
        this.cache.riskLabel=document.getElementById("risk-label");
        this.cache.evaluationDate=document.getElementById("evaluation-date");
        this.cache.evaluationTime=document.getElementById("evaluation-time");
        this.cache.summaryText=document.getElementById("summary-text");
        this.cache.criteriaGrid=document.getElementById("criteria-grid");
        this.cache.recommendationList=document.getElementById("recommendation-list");
        this.cache.inferenceFlow=document.getElementById("inference-flow");
        this.cache.newEvaluationButton=document.getElementById("new-evaluation-button");
        this.cache.homeButton=document.getElementById("home-button");
        this.cache.downloadReportButton=document.getElementById("download-report-button");
    },

    bindEvents(){
        this.cache.newEvaluationButton?.addEventListener(
            "click",
            ()=>window.location.href="evaluation.html"
        );

        this.cache.homeButton?.addEventListener(
            "click",
            ()=>window.location.href="index.html"
        );

        this.cache.downloadReportButton?.addEventListener(
            "click",
            ()=>window.print()
        );

        window.addEventListener(
            "resize",
            ()=>{
                this.resizeCanvas();
                this.createFlowLines();
            }
        );
    },

    async loadKnowledge(){
        const response=await fetch("data/knowledge.json");
        this.state.knowledge=await response.json();
    },

    readStoredEvaluation(){
        try{
            return JSON.parse(
                localStorage.getItem("evalioEvaluationResult")
            );
        }
        catch(error){
            console.warn("Evaluation result could not be parsed.",error);
            return null;
        }
    },

    buildResult(){
        if(this.state.stored?.response?.data){
            return this.mapBackendResult(
                this.state.stored
            );
        }

        return this.buildEmptyResult();
    },

    mapBackendResult(stored){
        const data=stored.response.data;
        const inference=data.inference || {};
        const evaluation=data.evaluation || {};
        const selectedFactIds=new Set(
            (inference.triggered_facts || []).map(
                fact=>fact.id
            )
        );
        const requestFactIds=new Set(stored.request?.facts || []);
        const matchedCriteriaIds=new Set(
            (inference.matched_criteria || []).map(
                criteria=>criteria.id
            )
        );
        const categoryCriteria=this.createCategoryCriteriaLookup(
            inference
        );
        const categories=this.state.knowledge.categories.map(
            category=>{
                const selected=category.facts.filter(
                    fact=>
                        selectedFactIds.has(fact.id) ||
                        requestFactIds.has(fact.id)
                ).length;
                const criteria=categoryCriteria[category.id];
                const matched=criteria
                    ? matchedCriteriaIds.has(criteria.id)
                    : false;

                return {
                    ...category,
                    selected,
                    total:category.facts.length,
                    matched,
                    criteria
                };
            }
        );

        return {
            selectedFactIds,
            categories,
            inference,
            evaluation,
            recommendation:data.recommendation || {items:[]},
            selectedFacts:selectedFactIds.size || requestFactIds.size,
            totalFacts:this.countFacts(),
            matchedCriteria:evaluation.matched_criteria || 0,
            totalCriteria:evaluation.total_criteria || this.countCriteria(inference),
            score:Math.round(evaluation.completion_percentage || 0),
            status:this.resolveStatus(
                inference.decision,
                evaluation.risk_level
            ),
            evaluatedAt:stored.evaluatedAt
        };
    },

    buildEmptyResult(){
        const categories=this.state.knowledge.categories.map(
            category=>({
                ...category,
                selected:0,
                total:category.facts.length,
                matched:false,
                criteria:null
            })
        );

        return {
            selectedFactIds:new Set(),
            categories,
            inference:{
                decision:{
                    name:"NOT_READY",
                    description:"Belum ada data evaluasi dari backend."
                },
                matched_rules:[],
                matched_criteria:[]
            },
            evaluation:{
                completion_percentage:0,
                matched_criteria:0,
                missing_criteria:8,
                total_criteria:8,
                risk_level:"HIGH"
            },
            recommendation:{items:[]},
            selectedFacts:0,
            totalFacts:this.countFacts(),
            matchedCriteria:0,
            totalCriteria:8,
            score:0,
            status:this.resolveStatus(
                {name:"NOT_READY",description:"Belum ada data evaluasi dari backend."},
                "HIGH"
            ),
            evaluatedAt:new Date().toISOString()
        };
    },

    createCategoryCriteriaLookup(inference){
        const lookup={};

        [
            ...(inference.matched_criteria || []),
            ...(inference.missing_criteria || [])
        ].forEach(
            criteria=>{
                lookup[criteria.category]=criteria;
            }
        );

        return lookup;
    },

    resolveStatus(decision,riskLevel){
        const name=decision?.name || "NOT_READY";
        const isReady=name==="READY";
        const isImprovement=name==="IMPROVEMENT";

        if(isReady){
            return {
                decision:"READY",
                subtitle:"Event Siap Diselenggarakan",
                description:decision.description,
                risk:"Risiko Rendah",
                riskLevel:"RENDAH",
                riskLabel:"Low Risk",
                tone:"success",
                icon:"check"
            };
        }

        if(isImprovement){
            return {
                decision:"IMPROVEMENT",
                subtitle:"Event Perlu Perbaikan",
                description:decision.description,
                risk:riskLevel==="LOW" ? "Risiko Rendah" : "Risiko Sedang",
                riskLevel:riskLevel==="LOW" ? "RENDAH" : "SEDANG",
                riskLabel:riskLevel==="LOW" ? "Low Risk" : "Medium Risk",
                tone:"warning",
                icon:"triangle-alert"
            };
        }

        return {
            decision:"NOT READY",
            subtitle:"Event Belum Siap Diselenggarakan",
            description:decision?.description || "Belum ada keputusan dari sistem.",
            risk:"Risiko Tinggi",
            riskLevel:"TINGGI",
            riskLabel:"High Risk",
            tone:"danger",
            icon:"x"
        };
    },

    render(){
        const result=this.state.result;

        this.renderStatus(result);
        this.renderMetrics(result);
        this.renderCriteria(result.categories);
        this.renderRecommendations(result.recommendation.items);
        this.renderInference(result);
    },

    renderStatus(result){
        const status=result.status;

        this.cache.decisionTitle.textContent=status.decision;
        this.cache.decisionSubtitle.textContent=status.subtitle;
        this.cache.decisionDescription.textContent=status.description;
        this.cache.scorePercent.textContent=`${result.score}%`;
        this.cache.riskPill.textContent=status.risk;
        this.cache.statusIcon.innerHTML=`<i data-lucide="${status.icon}"></i>`;

        this.cache.decisionTitle.className="";
        this.cache.statusIcon.className="status-icon";

        if(status.tone!=="success"){
            this.cache.decisionTitle.classList.add(status.tone);
            this.cache.statusIcon.classList.add(status.tone);
        }

        const circumference=2*Math.PI*88;
        this.cache.scoreRing.style.strokeDasharray=circumference;
        this.cache.scoreRing.style.strokeDashoffset=
            circumference-(result.score/100)*circumference;
    },

    renderMetrics(result){
        const date=new Date(result.evaluatedAt);
        const localeDate=date.toLocaleDateString(
            "id-ID",
            {day:"numeric",month:"long",year:"numeric"}
        );
        const localeTime=date.toLocaleTimeString(
            "id-ID",
            {hour:"2-digit",minute:"2-digit"}
        );

        this.cache.factsScore.textContent=
            `${result.selectedFacts} / ${result.totalFacts}`;
        this.cache.factsPercent.textContent=
            `${this.toDecimal((result.selectedFacts/result.totalFacts)*100)}%`;
        this.cache.categoriesScore.textContent=
            `${result.matchedCriteria} / ${result.totalCriteria}`;
        this.cache.categoriesPercent.textContent=
            `${this.toDecimal(result.evaluation.completion_percentage)}%`;
        this.cache.riskLevel.textContent=result.status.riskLevel;
        this.cache.riskLabel.textContent=result.status.riskLabel;
        this.cache.evaluationDate.textContent=localeDate;
        this.cache.evaluationTime.textContent=`${localeTime} WITA`;
        this.cache.summaryText.textContent=this.createSummary(result);
    },

    createSummary(result){
        const decision=result.inference.decision.name;
        const matched=result.matchedCriteria;
        const total=result.totalCriteria;

        if(decision==="READY"){
            return `Forward chaining menyimpulkan ${matched} dari ${total} kriteria terpenuhi. Event siap dilaksanakan dengan rekomendasi pemantauan akhir.`;
        }

        if(decision==="IMPROVEMENT"){
            return `Forward chaining menyimpulkan ${matched} dari ${total} kriteria terpenuhi. Event dapat dilanjutkan setelah rekomendasi prioritas ditangani.`;
        }

        return `Forward chaining menyimpulkan ${matched} dari ${total} kriteria terpenuhi. Event belum layak dilaksanakan sebelum aspek kritis diperbaiki.`;
    },

    renderCriteria(categories){
        this.cache.criteriaGrid.innerHTML=categories.map(
            category=>`
                <article class="criteria-card ${category.matched ? "high" : "low"}">
                    <div class="category-icon">
                        <i data-lucide="${category.icon}"></i>
                    </div>
                    <div>
                        <h4>${this.shortName(category.name)}</h4>
                        <strong>${category.selected} / ${category.total}</strong>
                    </div>
                    <span class="category-check">
                        <i data-lucide="${category.matched ? "check" : "minus"}"></i>
                    </span>
                </article>
            `
        ).join("");
    },

    renderRecommendations(items){
        const recommendations=items.length>0
            ? items.slice(0,3)
            : [
                {
                    recommendation:{
                        description:"Tidak ada rekomendasi perbaikan utama dari sistem."
                    },
                    priority:"low"
                }
            ];

        this.cache.recommendationList.innerHTML=recommendations.map(
            item=>`
                <article class="recommendation-item">
                    <span class="recommendation-dot"></span>
                    <p>${item.recommendation.description}</p>
                    <span class="priority-pill ${this.priorityClass(item.priority)}">
                        ${this.priorityLabel(item.priority)}
                    </span>
                </article>
            `
        ).join("");
    },

    renderInference(result){
        const globalRule=result.inference.matched_rules.find(
            rule=>rule.rule_type==="global"
        );
        const categoryRules=result.inference.matched_rules.filter(
            rule=>rule.rule_type==="category"
        );

        const steps=[
            {
                icon:"clipboard-list",
                iconClass:"pink",
                title:`${result.selectedFacts} Fakta Dipilih`,
                text:`Dari ${result.totalFacts} fakta repository`
            },
            {
                icon:"shield-check",
                iconClass:"purple",
                title:`${categoryRules.length} Rule Kategori`,
                text:`${result.matchedCriteria} kriteria terpenuhi`
            },
            {
                icon:"scale",
                iconClass:"purple",
                title:"Aturan Global",
                text:globalRule
                    ? `${globalRule.id} terpenuhi`
                    : "Tidak ada rule global cocok"
            },
            {
                icon:"check-circle-2",
                iconClass:"green",
                title:"Keputusan",
                text:result.status.decision
            }
        ];

        this.cache.inferenceFlow.innerHTML=steps.map(
            (step,index)=>`
                ${index>0 ? this.flowArrow() : ""}
                <article class="flow-card">
                    <div class="flow-icon ${step.iconClass}">
                        <i data-lucide="${step.icon}"></i>
                    </div>
                    <div>
                        <strong>${step.title}</strong>
                        <span>${step.text}</span>
                    </div>
                </article>
            `
        ).join("");
    },

    flowArrow(){
        return `
            <span class="flow-arrow">
                <i data-lucide="arrow-right"></i>
            </span>
        `;
    },

    shortName(name){
        return name==="Sumber Daya Manusia" ? "SDM" : name;
    },

    priorityClass(priority){
        return priority==="critical" ? "high" : priority;
    },

    priorityLabel(priority){
        const labels={
            critical:"Prioritas Kritis",
            high:"Prioritas Tinggi",
            medium:"Prioritas Sedang",
            low:"Prioritas Rendah"
        };

        return labels[priority] || "Prioritas";
    },

    countFacts(){
        return this.state.knowledge.categories.reduce(
            (sum,category)=>sum+category.facts.length,
            0
        );
    },

    countCriteria(inference){
        return (
            (inference.matched_criteria || []).length+
            (inference.missing_criteria || []).length
        ) || 8;
    },

    toDecimal(value){
        return Number.isInteger(value) ? value : value.toFixed(1);
    },

    setupCanvas(){
        if(!this.cache.canvas) return;

        this.cache.context=this.cache.canvas.getContext("2d");
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

        const count=22;
        const startY=this.cache.canvas.height*.11;

        for(let i=0;i<count;i++){
            this.state.flowLines.push({
                y:startY+i*5,
                speed:.18+Math.random()*.25,
                opacity:.035+Math.random()*.055,
                width:.8+Math.random()*1.2,
                phase:Math.random()*Math.PI*2,
                amplitude:14+Math.random()*34
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

                gradient.addColorStop(0,"rgba(255,154,31,0)");
                gradient.addColorStop(.18,`rgba(255,174,24,${line.opacity})`);
                gradient.addColorStop(.48,`rgba(255,214,32,${line.opacity*1.8})`);
                gradient.addColorStop(.80,`rgba(255,154,31,${line.opacity})`);
                gradient.addColorStop(1,"rgba(255,154,31,0)");

                context.beginPath();
                context.lineWidth=line.width;
                context.strokeStyle=gradient;

                for(let x=0;x<=canvas.width;x+=8){
                    const y=
                        line.y+
                        Math.sin((x/canvas.width)*Math.PI*3+line.phase)*line.amplitude+
                        Math.sin((x/canvas.width)*Math.PI*7+line.phase)*8;

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

        this.state.animationId=requestAnimationFrame(
            ()=>this.animateCanvas()
        );
    }

};

document.addEventListener(
    "DOMContentLoaded",
    ()=>ResultPage.init()
);

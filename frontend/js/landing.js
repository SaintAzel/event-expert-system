/*
========================================
Evalio Landing Controller
Version : 1.0
Sprint B1
========================================
*/

"use strict";

const LandingController = {

    cursorGlow:null,

    mouseX:0,

    mouseY:0,

    glowX:0,

    glowY:0,

    /*
    ========================================
    State
    ========================================
    */

    startButton: null,

    canvas: null,

    ctx: null,

    animationId: null,

    flowLines: [],

    /*
    ========================================
    Initialize
    ========================================
    */

    init() {

        this.cacheElements();

        this.bindEvents();

        this.setupCanvas();

        this.setupAnimations();

        this.setupParticles();

        this.setupMouseGlow();

    },

    /*
    ========================================
    Cache DOM
    ========================================
    */

    cacheElements() {

        this.cursorGlow =

            document.querySelector(

                ".cursor-glow"

            );

        this.startButton =
            document.querySelector(".hero-button");

        this.canvas =
            document.getElementById("wave-canvas");

    },

    /*
    ========================================
    Events
    ========================================
    */

    bindEvents() {

        this.startButton?.addEventListener(

            "click",

            () => this.handleNavigation()

        );

        window.addEventListener(

            "resize",

            () => {

                this.resizeCanvas();

                this.createFlowLines();

            }

        );

    },

    /*
    ========================================
    Navigation
    ========================================
    */

    handleNavigation() {

        window.location.href =
            "evaluation.html";

    },

    /*
    ========================================
    Canvas
    ========================================
    */

    setupCanvas() {

        if (!this.canvas) return;

        this.ctx =
            this.canvas.getContext("2d");

        this.resizeCanvas();

        this.createFlowLines();

        this.animateCanvas();

    },

    /*
    ========================================
    Resize
    ========================================
    */

    resizeCanvas() {

        this.canvas.width =
            window.innerWidth;

        this.canvas.height =
            window.innerHeight;

    },

    /*
    ========================================
    Flow Lines
    ========================================
    */

    createFlowLines(){

        this.flowLines=[];

        const count=42;

        const spacing=9;

        const startY=

            this.canvas.height*.50;

        for(

            let i=0;

            i<count;

            i++

        ){

            const line={

                y:

                    startY+

                    i*spacing,

                speed:

                    .22+

                    Math.random()*.18,

                opacity:

                    .055+

                    Math.random()*.08,

                width:

                    .65+

                    Math.random()*1.35,

                phase:

                    Math.random()*Math.PI*2,

                amplitude:

                    42+

                    Math.random()*58,

                segments:[]

            };

            const segmentCount=

                2+

                Math.floor(

                    Math.random()*3

                );

            for(

                let j=0;

                j<segmentCount;

                j++

            ){

                line.segments.push({

                    x:

                        Math.random()

                        *

                        this.canvas.width,

                    width:

                        180+

                        Math.random()*120,

                    height:

                        10+

                        Math.random()*12

                });

            }

            this.flowLines.push(line);

        }

    },

    /*
    ========================================
    Draw
    ========================================
    */

    drawFlow(){

        const ctx=this.ctx;

        ctx.clearRect(

            0,

            0,

            this.canvas.width,

            this.canvas.height

        );

        for(

            const line

            of

            this.flowLines

        ){

            ctx.beginPath();

            ctx.lineWidth=

                line.width;

            const gradient=

                ctx.createLinearGradient(

                    0,

                    line.y,

                    this.canvas.width,

                    line.y

                );

            gradient.addColorStop(0,"rgba(255,111,0,0)");
            gradient.addColorStop(.18,`rgba(255,139,0,${line.opacity})`);
            gradient.addColorStop(.46,`rgba(255,221,56,${line.opacity*2.3})`);
            gradient.addColorStop(.70,`rgba(255,126,0,${line.opacity*1.35})`);
            gradient.addColorStop(1,"rgba(255,95,0,0)");

            ctx.strokeStyle=gradient;

            for(

                let x=0;

                x<=this.canvas.width;

                x+=5

            ){

                let offset=0;

                for(

                    const segment

                    of

                    line.segments

                ){

                    if(

                        x>=segment.x

                        &&

                        x<=segment.x+

                        segment.width

                    ){

                        const t=

                            (

                                x-

                                segment.x

                            )

                            /

                            segment.width;

                        offset+=

                            Math.sin(

                                t*Math.PI

                            )

                            *

                            segment.height;

                    }

                }

                const wave=

                    Math.sin((x/this.canvas.width)*Math.PI*3.2+line.phase)*

                    line.amplitude+

                    Math.sin((x/this.canvas.width)*Math.PI*7.1+line.phase*.7)*

                    22;

                const y=

                    line.y+

                    offset+

                    wave;

                if(x===0)

                    ctx.moveTo(

                        x,

                        y

                    );

                else

                    ctx.lineTo(

                        x,

                        y

                    );

            }

            ctx.stroke();

        }

    },

    /*
    ========================================
    Animation
    ========================================
    */

    animateCanvas(){

        for(

            const line

            of

            this.flowLines

        ){

            for(

                const segment

                of

                line.segments

            ){

                segment.x+=

                    line.speed;

                if(

                    segment.x>

                    this.canvas.width+

                    segment.width

                ){

                    segment.x=

                        -segment.width;

                }

            }

            line.phase+=line.speed*.006;

        }

        this.drawFlow();

        this.animationId=

            requestAnimationFrame(

                ()=>this.animateCanvas()

            );

    },

    /*
    ========================================
    Placeholder
    ========================================
    */

    setupAnimations() {

        // Sprint C

    },

    setupParticles() {

        // Sprint D

    },

    setupMouseGlow(){

        if(!this.cursorGlow)return;

        this.mouseX=

            window.innerWidth/2;

        this.mouseY=

            window.innerHeight/2;

        this.glowX=

            this.mouseX;

        this.glowY=

            this.mouseY;

        document.addEventListener(

            "mousemove",

            (event)=>{

                this.mouseX=

                    event.clientX;

                this.mouseY=

                    event.clientY;

            }

        );

        const animate=()=>{

            this.glowX+=

                (

                    this.mouseX-

                    this.glowX

                )*.12;

            this.glowY+=

                (

                    this.mouseY-

                    this.glowY

                )*.12;

            this.cursorGlow.style.left=

                `${this.glowX}px`;

            this.cursorGlow.style.top=

                `${this.glowY}px`;

            requestAnimationFrame(

                animate

            );

        };

        animate();

    }

};

document.addEventListener(

    "DOMContentLoaded",

    () => LandingController.init()

);

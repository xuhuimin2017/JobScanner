<template>
  <q-layout view="hHh lpR fff" class="bg-white">

    <q-page-container>
      <q-page class="column items-center">
        <div class="container column items-center absolute">

          <div class="header full-width q-px-md">
            <q-toolbar class="bg-white text-grey-8">
              <q-toolbar-title shrink class="row items-center no-wrap">
                <q-btn no-caps rounded flat :ripple="false" size="1em" @click="$router.push({name: 'upload'})">
                  JobScanner
                </q-btn>
              </q-toolbar-title>
              <q-space />
              <q-btn round dense flat color="text-grey-7" icon="mdi-github" @click="openGithub"></q-btn>
            </q-toolbar>
          </div>

          <q-card flat bordered class="bg-card q-ma-lg bg-secondary">
            <moving-background class="absolute q-ma-"></moving-background>
            <q-card-section class="q-mt-md text-center text-primary">
              <div class="big-text text-weight-medium">Job Scanner</div>
              <div class="q-mt-md subtitle-text animate-float-enter">Upload Resumes, Analyze Skills and Get Jobs!</div>
            </q-card-section>
            <div>
              <q-card
                class="icon-card animate-scale-show-enter"
                :class="isProcessingStep ? 'moving-to-center' : ''"
                style="top:35%; left:4%; animation-delay: 200ms;"
              >
                <q-card-section>
                  <q-icon size="5em" name="img:icon-content/cv.svg"></q-icon>
                </q-card-section>
              </q-card>
              <q-card
                class="icon-card animate-scale-show-enter"
                :class="isProcessingStep ? 'moving-to-center' : ''"
                style="bottom:8%; left:14%; animation-delay: 500ms;"
              >
                <q-card-section>
                  <q-icon size="2.9em" name="img:icon-content/cv-cv.svg"></q-icon>
                </q-card-section>
              </q-card>
              <q-card
                class="icon-card animate-scale-show-enter"
                :class="isProcessingStep ? 'moving-to-center' : ''"
                style="top:26%; right: 2%; animation-delay: 700ms;"
              >
                <q-card-section>
                  <q-icon size="2.5em" name="img:icon-content/recruitment.svg"></q-icon>
                </q-card-section>
              </q-card>
              <q-card
                class="icon-card animate-scale-show-enter"
                :class="isProcessingStep ? 'moving-to-center' : ''"
                style="bottom:14%; right: 12%; animation-delay: 000ms;"
              >
                <q-card-section>
                  <q-icon size="4em" name="img:icon-content/portfolio.svg"></q-icon>
                </q-card-section>
              </q-card>
            </div>
          </q-card>

          <q-card class="main-card" :class="isUploadingStep ? 'enlarge' : ''">
            <q-card-section style="padding: 0">
              <router-view />
            </q-card-section>
          </q-card>

          <div class="footer absolute-bottom text-primary non-selectable text-center q-pa-md">
            <span class="footer-credit" @mouseenter="heartSuffix=''" @mouseleave="heartSuffix='-outline'">
              <q-icon :name="'mdi-heart'+heartSuffix"></q-icon>
              Created by <a href="#">Guangxue Wen</a>, <a href="#">Huimin Xu</a>, <a href="#">Lingfei Wu</a>
            </span>
          </div>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import MovingBackground from 'components/MovingBackground.vue'
import { openInNewTab } from 'src/utils/dom'

@Component({
  components: { MovingBackground }
})
export default class CardLayout extends Vue {
  currentStep = ''
  heartSuffix = '-outline'

  get style () {
    return {
      height: `${this.$q.screen.height} px`
    }
  }

  openGithub () {
    openInNewTab('https://github.com/wenoptics/JobScanner')
  }

  get isProcessingStep () {
    return this.currentStep === 'processing'
  }

  get isUploadingStep () {
    return this.currentStep === 'uploading'
  }
}
</script>

<style scoped lang="scss">
.bg-card {
  position: relative;
  height: 40vh;
  min-height: 18em;
  max-height: 25em;
  width: 70vw;
  max-width: 55em;
  border-radius: 1.75em;
  border-width: 0;
  transition: all 800ms;
}

.main-card {
  position: relative;
  top: -11.5em; // Negative number so that we have some overlap with the atop item
  border-radius: 1.5em;
  box-shadow: 0 5px 20px 2px #c3c3c34d;
  transition: all 800ms cubic-bezier(0.175, 0.885, 0.320, 1.275); /* easeOutBack */

  &.enlarge {
    transform: scale(1.1);
  }
}

.container.content-mode {
  .bg-card {
    max-width: 80em;
    height: 12em;
    min-height: 12em;
  }
  .main-card {
    top: 0
  }
}

.icon-card {
  position: absolute;
  border-radius: 1.75em;
  border-width: 0;
  box-shadow: 0 11px 12px 0 #a7edff55;
  animation: buyoo-buyoo infinite, bubble-scale infinite;
  animation-duration: 1.5s, 3s;
  transition: all 1s;
  :hover {
    animation: swag-rotate 1s;
    animation-timing-function: linear;
  }
}

.moving-to-center {
  animation: moving-to-center 700ms;
  animation-delay: 0ms !important;
  animation-iteration-count: 1;
  animation-timing-function: cubic-bezier(0.1, -0.2, 0.2, 0);
  animation-fill-mode: forwards;  // Stay at the finish frame
}

.big-text {
  font-size: x-large;
}

.footer {
  bottom: 0;
}

.animate-float-enter {
  opacity: 0;
  animation: float-up 1000ms;
  animation-delay: 1000ms;
  animation-fill-mode: forwards;  // Stay at the finish frame
}

.animate-scale-show-enter {
  transform: scale(0);
  animation: scale-show 400ms;
  animation-delay: 500ms;
  animation-timing-function: cubic-bezier(0.175, 0.885, 0.320, 1.275); /* easeOutBack */;
  animation-fill-mode: forwards;  // Stay at the finish frame
}

.subtitle-text {
  font-size: medium;
}

@keyframes buyoo-buyoo {
  0% {
    transform: translateY(0);
  }
  55% {
    transform: translateY(2px);
  }
  100% {
    transform: translateY(0);
  }
}

@keyframes moving-to-center {
  100% {
    top: 100%;
    right: 50%;
    left: 50%;
    bottom: 0;
    transform: scale(0, 0) rotateZ(30deg);
  }
}

@keyframes float-up {
  0% {
    transform: translateY(2em);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes scale-show {
  0% {
    transform: scale(0.6);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes bubble-scale {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes swag-rotate {
  0% {
    transform: rotateZ(0);
  }
  33% {
    transform: rotateZ(2deg);
  }
  66% {
    transform: rotateZ(-2deg);
  }
  100% {
    transform: rotateZ(0);
  }
}

</style>

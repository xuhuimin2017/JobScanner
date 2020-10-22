<template>
  <div class="column container items-center absolute">
    <q-card flat bordered class="bg-card q-ma-lg bg-secondary">
      <moving-background class="absolute q-ma-"></moving-background>
      <q-card-section class="q-mt-md text-center big-text text-primary text-weight-medium">
        Upload Resumes, Analyze Skills and Get Jobs!
      </q-card-section>
      <div>
        <q-card
          class="icon-card"
          :class="isProcessingStep ? 'moving-to-center' : ''"
          style="top:35%; left:4%; animation-delay: 200ms;"
        >
          <q-card-section>
            <q-icon size="5em" name="img:icon-content/cv.svg">
            </q-icon>
          </q-card-section>
        </q-card>
        <q-card
          class="icon-card"
          :class="isProcessingStep ? 'moving-to-center' : ''"
          style="bottom:8%; left:14%; animation-delay: 500ms;"
        >
          <q-card-section>
            <q-icon size="2.9em" name="img:icon-content/cv-cv.svg">
            </q-icon>
          </q-card-section>
        </q-card>
        <q-card
          class="icon-card"
          :class="isProcessingStep ? 'moving-to-center' : ''"
          style="top:26%; right: 2%; animation-delay: 700ms;"
        >
          <q-card-section>
            <q-icon size="2.5em" name="img:icon-content/recruitment.svg">
            </q-icon>
          </q-card-section>
        </q-card>
        <q-card
          class="icon-card"
          :class="isProcessingStep ? 'moving-to-center' : ''"
          style="bottom:14%; right: 12%; animation-delay: 000ms;"
        >
          <q-card-section>
            <q-icon size="4em" name="img:icon-content/portfolio.svg">
            </q-icon>
          </q-card-section>
        </q-card>
      </div>
    </q-card>

    <q-card class="main-card" :class="isProcessingStep ? 'enlarge' : ''">
      <q-card-section class="q-ma-md absolute-full">
        <upload-view @onProcessing="isProcessingStep = true"></upload-view>
      </q-card-section>
    </q-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import UploadView from 'components/UploadView.vue'
import MovingBackground from "components/MovingBackground.vue";

@Component({
  components: {MovingBackground, UploadView }
})
export default class LandingView extends Vue {
  isProcessingStep = false
}
</script>

<style scoped lang="scss">
.bg-card {
  position: relative;
  min-height: 250px;
  height: 40vh;
  max-height: 360px;
  width: 70vw;
  max-width: 55em;
  border-radius: 1.75em;
  border-width: 0;
}

.main-card {
  position: relative;
  bottom: 12em;
  width: 25em;
  min-height: 14em;
  border-radius: 1.5em;
  box-shadow: 0px 5px 20px 2px #c3c3c34d;
  transition: all 500ms;

  &.enlarge {
    transform: scale(1.1);
  }
}

.icon-card {
  position: absolute;
  border-radius: 1.75em;
  border-width: 0;
  box-shadow: 0px 11px 12px 0px #a7edff55;
  animation: buyoo-buyoo infinite 1.5s;
  :hover {
    transform: scale(1.05, 1.05);
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
    bottom: 0%;
    transform: scale(0, 0) rotateZ(30deg);
  }
}
</style>

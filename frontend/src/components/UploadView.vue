<template>
  <div class="column container items-center">
    <q-card flat bordered class="bg-card q-ma-lg bg-secondary">
      <q-card-section class="q-mt-md text-center big-text text-primary text-weight-medium">
        Upload Resumes, Analyze Skills and Get Jobs!
      </q-card-section>
      <div>
        <q-card
          class="icon-card"
          :class="currentStep === 'processing' ? 'moving-to-center' : ''"
          style="top:35%; left:4%; animation-delay: 200ms;"
        >
          <q-card-section>
            <q-icon size="5em" name="img:icon-content/cv.svg">
            </q-icon>
          </q-card-section>
        </q-card>
        <q-card
          class="icon-card"
          :class="currentStep === 'processing' ? 'moving-to-center' : ''"
          style="bottom:8%; left:14%; animation-delay: 500ms;"
        >
          <q-card-section>
            <q-icon size="2.9em" name="img:icon-content/cv-cv.svg">
            </q-icon>
          </q-card-section>
        </q-card>
        <q-card
          class="icon-card"
          :class="currentStep === 'processing' ? 'moving-to-center' : ''"
          style="top:26%; right: 2%; animation-delay: 700ms;"
        >
          <q-card-section>
            <q-icon size="2.5em" name="img:icon-content/recruitment.svg">
            </q-icon>
          </q-card-section>
        </q-card>
        <q-card
          class="icon-card"
          :class="currentStep === 'processing' ? 'moving-to-center' : ''"
          style="bottom:14%; right: 12%; animation-delay: 000ms;"
        >
          <q-card-section>
            <q-icon size="4em" name="img:icon-content/portfolio.svg">
            </q-icon>
          </q-card-section>
        </q-card>
      </div>
    </q-card>
    <q-card class="upload-card">
      <q-card-section class="absolute-full">

        <!--Step1: Show uploading form-->
        <div
          v-if="currentStep === 'beforeUpload'"
          class="drop-area full-width full-height column flex-center"
        >
          <q-file
            v-model="file"
            label="Browse files"
            outlined
            dense
            style="width: 10em"
            accept=".pdf, image/*"
            @input="cmdUpload"
          >
            <template v-slot:prepend>
              <q-icon name="attach_file" />
            </template>
          </q-file>
        </div>

        <!--Step2: Show uploading progress-->
        <div
          v-if="currentStep === 'uploading'"
          class="full-width full-height row flex-center"
        >
          <div class="row items-center q-gutter-sm">
            <div><q-btn
              :disable="!error.upload"
              class="style-widget"
              round unelevated dense icon="pause">
            </q-btn></div>
            <div><q-circular-progress
              reverse
              indeterminate
              size="8em"
              :thickness="0.09"
              show-value
              :color="error.upload ? 'negative' : 'primary'"
              track-color="grey-3"
              class="q-ma-md"
            >
              <span class="text-center text-subtitle1">
                {{ error.upload ? 'Error' : 'Uploading' }}
              </span>
            </q-circular-progress></div>
            <div>
              <q-btn
                v-if="error.upload"
                title="Reset and retry"
                class="style-widget"
                round unelevated dense icon="restore"
                @click="cmdReset">
              </q-btn>
              <q-btn v-else class="style-widget" round unelevated dense icon="close"></q-btn>
            </div>
          </div>
          <div v-if="error.upload" class="text-negative text-center">
            Upload failure: {{ error.upload }}
          </div>
          <div v-else class="ellipsis" :title="filename">
            Uploading your resume:
            <span class="q-ml-sm filename">{{ filename }}</span>
          </div>
        </div>

        <!--Step3: Show processing progress-->
        <div
          v-if="currentStep === 'processing'"
          class="full-width full-height row flex-center"
        >
          <div class="row items-center q-gutter-sm">
            <div><q-btn disable class="style-widget" round unelevated dense icon="pause"></q-btn></div>
            <div><q-circular-progress
              reverse
              :indeterminate="!error.processing"
              size="8em"
              :thickness="0.09"
              show-value
              color="primary"
              track-color="grey-3"
              class="q-ma-md"
            >
              <span class="text-center text-subtitle1">Processing</span>
            </q-circular-progress></div>
            <div><q-btn disable class="style-widget" round unelevated dense icon="close"></q-btn></div>
          </div>
          <div class="ellipsis">
            <template v-if="error.processing" class="text-red">{{ error.processing }}</template>
            <template v-else>Processing... will be right soon!</template>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { getJobsFromResume, uploadResume } from 'src/api/app'
import { RecommendationModel } from 'components/models'

interface ErrorStage {
  beforeUpload: string | null,
  upload: string | null,
  processing: string | null
}

@Component
export default class UploadView extends Vue {
  isUploading = false
  file: File | null = null
  currentStep = 'beforeUpload'
  error: ErrorStage = {
    beforeUpload: null,
    upload: null,
    processing: null
  }

  get filename () {
    return this.file?.name
  }

  // mounted () {}

  cmdUpload () {
    this.isUploading = true
    this.currentStep = 'uploading'
    console.log(this.file)

    return uploadResume(this.file)
      .catch((e: string) => {
        console.error('Resume uploading failed!', e)
        this.error.upload = e
        throw e
      })
      .then(s3FileId => {
        console.log('Resume uploading successfully!', s3FileId)
        this.currentStep = 'processing'
        return getJobsFromResume(s3FileId)
      }).catch((e: string) => {
        console.error('Processing resume failed!', e)
        this.error.processing = e
        throw e
      }).then((data: RecommendationModel) => {
        return this.$router.push({
          name: 'result',
          params: { recommendationData: JSON.stringify(data) }
        })
      }).finally(() => {
        this.isUploading = false
      })
  }

  cmdReset () {
    this.error.beforeUpload = null
    this.error.upload = null
    this.error.processing = null
    this.isUploading = false
    this.file = null
    this.currentStep = 'beforeUpload'
  }
}
</script>

<style lang="scss" scoped>

.container {
  position: absolute;
}

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

.upload-card {
  position: relative;
  bottom: 12em;
  width: 25em;
  min-height: 14em;
  border-radius: 1.5em;
  box-shadow: 0px 5px 20px 2px #c3c3c34d;
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
  animation: moving-to-center 1s;
  animation-delay: 0ms;
  animation-iteration-count: 1;
  animation-timing-function: cubic-bezier(0.1, -0.2, 0.2, 0);
  animation-fill-mode: forwards;  // Stay the finish frame
}

.big-text {
  font-size: x-large;
}

.filename {
  font-family: sans-serif, 'Helvetica Neue', '-apple-system', 'Roboto', Helvetica, Arial
}

.drop-area {
  border: dashed #e4e4e4 5px;
  &.engaging {
    //animation: border-rotating 4s infinite linear;
  }
}

@keyframes border-rotating {
  0% {
    background-position: 0 0, 100% 100%, 0 100%, 100% 0;
  }
  100% {
    background-position: 100% 0, 0 100%, 0 0, 100% 100%;
  }
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

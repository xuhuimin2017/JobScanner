<template>
  <div class="relative-position q-pa-md">
    <transition
      mode="out-in"
      appear
      enter-active-class="animated bounceIn"
      leave-active-class="animated fadeOut"
    >
      <!--Step1: Show uploading form-->
      <div
        key="StageInit"
        v-if="isStageInit"
        class="drop-area column flex-center"
        style="width: 21em; min-height: 12em;"
      >
        <q-file
          v-model="file"
          class="non-selectable"
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
        key="StageUploading"
        v-if="isStageUploading"
        class="row flex-center"
        style="width: 23em; min-height: 12em;"
      >
        <div class="row items-center q-gutter-sm">
          <div><q-btn
            disable class="style-widget"
            round unelevated dense icon="pause">
          </q-btn></div>
          <div><q-circular-progress
            reverse
            :indeterminate="isProgressing"
            :value="isProgressing ? 0 : 100"
            size="8em"
            :thickness="0.09"
            show-value
            :color="errorMessage ? 'negative' : 'primary'"
            track-color="grey-3"
            class="q-ma-md"
          >
            <span class="text-center text-subtitle1">
              {{ errorMessage ? 'Error' : 'Uploading' }}
            </span>
          </q-circular-progress></div>
          <div>
            <q-btn
              v-if="errorMessage"
              title="Reset and retry"
              class="style-widget"
              round unelevated dense icon="restore"
              @click="cmdReset">
            </q-btn>
            <q-btn v-else class="style-widget" round unelevated dense icon="close"></q-btn>
          </div>
        </div>
        <div v-if="errorMessage" class="text-negative text-center">
          Upload failure: {{ errorMessage }}
        </div>
        <div v-else class="ellipsis" :title="filename">
          Uploading your resume:
          <span class="q-ml-sm filename">{{ filename }}</span>
        </div>
      </div>

      <!--Step3: Show processing progress-->
      <div
        key="StageProcessing"
        v-if="isStageProcessing"
        class="row flex-center"
        style="width: 21em; min-height: 12em;"
      >
        <div class="row items-center q-gutter-sm">
          <div><q-btn disable class="style-widget" round unelevated dense icon="pause"></q-btn></div>
          <div><q-circular-progress
            reverse
            :indeterminate="!errorMessage"
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
          <template v-if="errorMessage" class="text-red">{{ errorMessage }}</template>
          <template v-else>Processing... will be right soon!</template>
        </div>
      </div>
    </transition>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator'
import { getJobsFromResume, uploadResume } from 'src/api/app'
import { RecommendationModel } from 'components/models'

export const enum Stage {
  initialized = 1,
  uploading,
  processing
}

@Component
export default class UploadView extends Vue {
  isProgressing = false
  file: File | null = null
  currentStep: Stage = Stage.initialized
  errorMessage: string | null = null

  get filename () {
    return this.file?.name
  }

  get isStageInit () {
    return this.currentStep === Stage.initialized
  }

  get isStageUploading () {
    return this.currentStep === Stage.uploading
  }

  get isStageProcessing () : boolean {
    return this.currentStep === Stage.processing
  }

  setStep (val: Stage) {
    if (this.currentStep === val) return
    this.currentStep = val
  }

  @Watch('currentStep')
  onStep () {
    if (this.isStageProcessing) {
      this.$emit('onProcessing')
    }
    if (this.isStageUploading) {
      this.$emit('onUploading')
    }
  }

  cmdUpload () {
    this.isProgressing = true
    this.setStep(Stage.uploading)
    console.log('file', this.file)

    return uploadResume(this.file)
      .catch((e: string) => {
        console.error('Resume uploading failed!', e)
        this.errorMessage = e
        throw e
      })
      .then(s3FileId => {
        console.log('Resume uploading successfully!', s3FileId)
        this.setStep(Stage.processing)
        return getJobsFromResume(s3FileId)
      }).catch((e: string) => {
        console.error('Processing resume failed!', e)
        this.errorMessage = e
        throw e
      }).then((data: RecommendationModel) => {
        return this.$router.push({
          name: 'result',
          params: { recommendationData: JSON.stringify(data) }
        })
      }).finally(() => {
        this.isProgressing = false
      })
  }

  cmdReset () {
    this.errorMessage = null
    this.isProgressing = false
    this.file = null
    this.setStep(Stage.initialized)
  }
}
</script>

<style lang="scss" scoped>
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
</style>

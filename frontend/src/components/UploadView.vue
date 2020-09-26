<template>
  <div class="column container items-center">
    <q-card flat bordered class="bg-card q-ma-lg bg-secondary">
      <q-card-section class="text-center big-text text-primary">
        Upload, Analyze and Get Hired!
      </q-card-section>
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
            <div><q-btn :disable="error.upload" class="style-widget" round unelevated dense icon="pause"></q-btn></div>
            <div><q-circular-progress
              reverse
              :value="uploadPercentage"
              size="8em"
              :thickness="0.09"
              show-value
              :color="error.upload ? 'negative' : 'primary'"
              track-color="grey-3"
              class="q-ma-md"
            >
              <span class="text-center text-subtitle1">
                {{ error.upload ? 'Error' : `${uploadPercentage}%` }}
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
              indeterminate
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
            Processing... will be right soon!
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

@Component
export default class UploadView extends Vue {
  isUploading: boolean = false
  uploadPercentage = 45
  file: File | null = null
  currentStep = 'beforeUpload'
  error = {
    beforeUpload: false,
    upload: false,
    processing: false
  }

  get filename() {
    return this.file?.name
  }

  cmdUpload() {
    this.isUploading = true
    const formData = new FormData();
    this.currentStep = 'uploading'
    formData.append('file', this.file);
    console.log(this.file)

    this.$axios.post( '/file-progress',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: ( progressEvent ) => {
          this.uploadPercentage = ( Math.round( ( progressEvent.loaded / progressEvent.total ) * 100 ))
          console.log('onUploadProgress', progressEvent)
        }
      })
      .then(() => {
        console.log('SUCCESS!!');
        this.currentStep = 'processing'
    })
      .catch(e => {
        console.log('FAILURE!!');
        this.error.upload = e
      })
    .finally(() => {})
  }

  cmdReset() {
    this.error.beforeUpload = false
    this.error.upload = false
    this.error.processing = false
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
  height: 35vh;
  width: 70vw;
  max-width: 50em;
  border-radius: 1.75em;
  border-width: 0;
}

.upload-card {
  position: relative;
  bottom: 12em;
  width: 25em;
  height: 14em;
  border-radius: 1.5em;
  box-shadow: 0px 5px 20px 2px #c3c3c34d;
}

.big-text {
  font-size: x-large;
  font-weight: 1000;
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

</style>

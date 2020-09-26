<template>
  <div class="column container items-center">
    <q-card flat bordered class="q-ma-lg bg-card">
      <q-card-section class="text-center big-text text-grey">
        Upload, Analyze and Get Hired!
      </q-card-section>
    </q-card>
    <q-card class="upload-card">
      <q-card-section class="absolute-full">
        <div v-if="!isUploading" class="drop-area full-width full-height column flex-center">
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

        <div v-else class="full-width full-height column flex-center">
          <!--Show upload loading-->
          <div class="row items-center q-gutter-md">
            <div><q-btn color="grey" round dense icon="pause"></q-btn></div>
            <div><q-circular-progress
              reverse
              :value="uploadPercentage"
              size="8em"
              :thickness="0.1"
              show-value
              color="light-blue"
              class="q-ma-md"
            >
              <span class="text-center text-subtitle1">{{ uploadPercentage }}%</span>
            </q-circular-progress></div>
            <div><q-btn color="grey" round dense icon="close"></q-btn></div>
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

  cmdUpload() {
    this.isUploading = true
    const formData = new FormData();
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
    })
      .catch(() => {
        console.log('FAILURE!!');
      })
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
}

.upload-card {
  position: relative;
  bottom: 12em;
  width: 25em;
  height: 14em;
}

.big-text {
  font-size: x-large;
  font-weight: 1000;
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

<template>
  <q-page class="column items-center">
    <upload-view></upload-view>
  </q-page>
</template>

<script lang="ts">
import UploadView from 'components/UploadView.vue'
import { Vue, Component } from 'vue-property-decorator'

@Component({
  components: { UploadView }
})
export default class UploadPage extends Vue {

}
</script>

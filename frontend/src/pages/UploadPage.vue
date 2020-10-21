<template>
  <q-page class="column items-center">
    <landing-view></landing-view>
  </q-page>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import LandingView from 'components/LandingView.vue'

@Component({
  components: { LandingView }
})
export default class UploadPage extends Vue {

}
</script>

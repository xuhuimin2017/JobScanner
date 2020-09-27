<template>
  <q-page class="column items-center">
    <listing-view></listing-view>
  </q-page>
</template>

<script lang="ts">
import ListingView from 'components/ListingView.vue'
import { Vue, Component } from 'vue-property-decorator'

@Component({
  components: { ListingView }
})
export default class UploadPage extends Vue {

}
</script>

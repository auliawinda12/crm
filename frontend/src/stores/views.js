import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'
import { reactive, ref } from 'vue'

export const viewsStore = defineStore('crm-views', (state) => ({
	let viewsByName = reactive({})
	let pinnedViews = ref([])
	let publicViews = ref([])
	let standardViews = ref({})
	const defaultView = ref(null)
	const hideUnassignedEmailLeads = ref(false)

	// Views
	const views = createResource({
		url: 'crm.api.views.get_views',
		params: { doctype: state.doctype || '' },
		cache: 'crm-views',
		initialData: [],
		auto: true,
		transform(views) {
			pinnedViews.value = []
			publicViews.value = []
			defaultView.value = null
			for (let view of views) {
				viewsByName[view.name] = view
				view.type = view.type || 'list'
				if (view.pinned) {
					pinnedViews.value?.push(view)
				}
				if (view.public) {
					publicViews.value?.push(view)
				}
				if (view.is_standard && view.dt) {
					standardViews.value[view.dt + ' ' + view.type] = view
				}
				if (view.is_default) {
					defaultView.value = view
				}
			}
			return views
		},
	})

	// Actions
	const setHideUnassignedEmailLeads = (enabled) => {
		hideUnassignedEmailLeads.value = enabled
	}

	return {
		views,
		defaultView,
		viewsByName,
		pinnedViews,
		publicViews,
		standardViews,
		hideUnassignedEmailLeads,
		setHideUnassignedEmailLeads,
		reload,
		getView,
		getDefaultView,
		getPinnedViews,
		getPublicViews,
	}
})

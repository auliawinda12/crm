import { io } from 'socket.io-client'
import { socketio_port } from '../../../../sites/common_site_config.json'
import { getCachedListResource, getCachedResource } from 'frappe-ui'

export function initSocket() {
  const host = window.location.hostname
  const isLocalhost =
    host === 'localhost' || host === '127.0.0.1' || host.endsWith('.localhost')
  const url = `${window.location.protocol}//${host}:${socketio_port}`
  const transportOptions = isLocalhost
    ? {
        transports: ['polling'],
        upgrade: false,
      }
    : {}

  let socket = io(url, {
    withCredentials: true,
    reconnectionAttempts: 5,
    ...transportOptions,
  })
  socket.on('refetch_resource', (data) => {
    if (data.cache_key) {
      let resource =
        getCachedResource(data.cache_key) ||
        getCachedListResource(data.cache_key)
      if (resource) {
        resource.reload()
      }
    }
  })
  return socket
}

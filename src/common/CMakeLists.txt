add_library(common_buffer_obj OBJECT
  buffer.cc)

add_library(common_texttable_obj OBJECT
  TextTable.cc)

add_library(common_prioritycache_obj OBJECT
  PriorityCache.cc)

set(common_srcs
  AsyncOpTracker.cc
  BackTrace.cc
  ConfUtils.cc
  Cycles.cc
  DecayCounter.cc
  Finisher.cc
  Formatter.cc
  Graylog.cc
  HTMLFormatter.cc
  HeartbeatMap.cc
  LogClient.cc
  LogEntry.cc
  Mutex.cc
  OutputDataSocket.cc
  PluginRegistry.cc
  Readahead.cc
  SloppyCRCMap.cc
  SubProcess.cc
  Thread.cc
  Throttle.cc
  Timer.cc
  TracepointProvider.cc
  TrackedOp.cc
  WorkQueue.cc
  address_helper.cc
  admin_socket.cc
  admin_socket_client.cc
  assert.cc
  bit_str.cc
  blkdev.cc
  bloom_filter.cc
  ceph_argparse.cc
  ceph_context.cc
  ceph_crypto.cc
  ceph_crypto_cms.cc
  ceph_frag.cc
  ceph_fs.cc
  ceph_hash.cc
  ceph_json.cc
  ceph_strings.cc
  ceph_time.cc
  cmdparse.cc
  code_environment.cc
  common_init.cc
  compat.cc
  condition_variable_debug.cc
  config.cc
  config_values.cc
  dns_resolve.cc
  dout.cc
  entity_name.cc
  environment.cc
  errno.cc
  escape.cc
  fd.cc
  fs_types.cc
  hex.cc
  histogram.cc
  hobject.cc
  hostname.cc
  ipaddr.cc
  iso_8601.cc
  linux_version.c
  lockdep.cc
  mempool.cc
  mime.c
  mutex_debug.cc
  numa.cc
  options.cc
  page.cc
  perf_counters.cc
  perf_counters_collection.cc
  perf_histogram.cc
  pick_address.cc
  random_string.cc
  reverse.c
  run_cmd.cc
  scrub_types.cc
  shared_mutex_debug.cc
  signal.cc
  snap_types.cc
  str_list.cc
  str_map.cc
  strtol.cc
  types.cc
  url_escape.cc
  utf8.c
  util.cc
  version.cc
  xattr.c)

set_source_files_properties(${CMAKE_SOURCE_DIR}/src/common/version.cc
  APPEND PROPERTY OBJECT_DEPENDS ${CMAKE_BINARY_DIR}/src/include/ceph_ver.h)

if(HAS_VTA)
  set_source_files_properties(
    config.cc
    options.cc
    PROPERTIES COMPILE_FLAGS -fno-var-tracking-assignments)
endif()

if(FREEBSD)
  list(APPEND common_srcs freebsd_errno.cc)
elseif(APPLE)
  list(APPEND common_srcs darwin_errno.cc)
elseif(SUN)
  list(APPEND common_srcs solaris_errno.cc)
elseif(AIX)
  list(APPEND common_srcs aix_errno.cc)
endif()

if(WITH_LTTNG AND WITH_EVENTTRACE)
  message(STATUS " Using EventTrace class.")
  add_definitions("-DWITH_EVENTTRACE")
  list(APPEND common_srcs EventTrace.cc)
endif()

add_library(common-common-objs OBJECT
  ${common_srcs})
# for options.cc
target_compile_definitions(common-common-objs PRIVATE
  "CEPH_LIBDIR=\"${CMAKE_INSTALL_FULL_LIBDIR}\""
  "CEPH_PKGLIBDIR=\"${CEPH_INSTALL_FULL_PKGLIBDIR}\""
  "CEPH_DATADIR=\"${CEPH_INSTALL_DATADIR}\"")

set(common_mountcephfs_srcs
  armor.c
  safe_io.c
  module.c
  addr_parsing.c)
add_library(common_mountcephfs_objs OBJECT
  ${common_mountcephfs_srcs})


set(crc32_srcs
  crc32c.cc
  crc32c_intel_baseline.c
  sctp_crc32.c)

if(HAVE_INTEL)
  list(APPEND crc32_srcs
    crc32c_intel_fast.c)
  if(HAVE_GOOD_YASM_ELF64)
    list(APPEND crc32_srcs
      crc32c_intel_fast_asm.s
      crc32c_intel_fast_zero_asm.s)
  endif(HAVE_GOOD_YASM_ELF64)
elseif(HAVE_POWER8)
  list(APPEND crc32_srcs
    crc32c_ppc.c)
  if(HAVE_PPC64LE)
    list(APPEND crc32_srcs
      crc32c_ppc_asm.S
      crc32c_ppc_fast_zero_asm.S)
  endif(HAVE_PPC64LE)
elseif(HAVE_ARMV8_CRC)
  list(APPEND crc32_srcs
    crc32c_aarch64.c)
endif(HAVE_INTEL)

add_library(crc32 ${crc32_srcs})
if(HAVE_ARMV8_CRC)
  set_target_properties(crc32 PROPERTIES
    COMPILE_FLAGS "${CMAKE_C_FLAGS} ${ARMV8_CRC_COMPILE_FLAGS}")
endif()
target_link_libraries(crc32
  arch)

add_library(common_utf8 STATIC utf8.c)

if(HAVE_KEYUTILS)
  set(parse_secret_srcs
    secret.c)
  add_library(parse_secret_objs OBJECT ${parse_secret_srcs})
endif()

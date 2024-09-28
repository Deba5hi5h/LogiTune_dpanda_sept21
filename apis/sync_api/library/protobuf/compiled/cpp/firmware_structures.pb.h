// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: firmware_structures.proto

#ifndef PROTOBUF_INCLUDED_firmware_5fstructures_2eproto
#define PROTOBUF_INCLUDED_firmware_5fstructures_2eproto

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 3006000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 3006000 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/inlined_string_field.h>
#include <google/protobuf/metadata.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
#include "common.pb.h"
#include "product_state_structures.pb.h"
// @@protoc_insertion_point(includes)
#define PROTOBUF_INTERNAL_EXPORT_protobuf_firmware_5fstructures_2eproto 

namespace protobuf_firmware_5fstructures_2eproto {
// Internal implementation detail -- do not use these members.
struct TableStruct {
  static const ::google::protobuf::internal::ParseTableField entries[];
  static const ::google::protobuf::internal::AuxillaryParseTableField aux[];
  static const ::google::protobuf::internal::ParseTable schema[2];
  static const ::google::protobuf::internal::FieldMetadata field_metadata[];
  static const ::google::protobuf::internal::SerializationTable serialization_table[];
  static const ::google::protobuf::uint32 offsets[];
};
void AddDescriptors();
}  // namespace protobuf_firmware_5fstructures_2eproto
namespace logi {
namespace proto {
class FirmwareUpdateProgress;
class FirmwareUpdateProgressDefaultTypeInternal;
extern FirmwareUpdateProgressDefaultTypeInternal _FirmwareUpdateProgress_default_instance_;
class LatestDeviceFirmwareInfo;
class LatestDeviceFirmwareInfoDefaultTypeInternal;
extern LatestDeviceFirmwareInfoDefaultTypeInternal _LatestDeviceFirmwareInfo_default_instance_;
}  // namespace proto
}  // namespace logi
namespace google {
namespace protobuf {
template<> ::logi::proto::FirmwareUpdateProgress* Arena::CreateMaybeMessage<::logi::proto::FirmwareUpdateProgress>(Arena*);
template<> ::logi::proto::LatestDeviceFirmwareInfo* Arena::CreateMaybeMessage<::logi::proto::LatestDeviceFirmwareInfo>(Arena*);
}  // namespace protobuf
}  // namespace google
namespace logi {
namespace proto {

// ===================================================================

class LatestDeviceFirmwareInfo : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:logi.proto.LatestDeviceFirmwareInfo) */ {
 public:
  LatestDeviceFirmwareInfo();
  virtual ~LatestDeviceFirmwareInfo();

  LatestDeviceFirmwareInfo(const LatestDeviceFirmwareInfo& from);

  inline LatestDeviceFirmwareInfo& operator=(const LatestDeviceFirmwareInfo& from) {
    CopyFrom(from);
    return *this;
  }
  #if LANG_CXX11
  LatestDeviceFirmwareInfo(LatestDeviceFirmwareInfo&& from) noexcept
    : LatestDeviceFirmwareInfo() {
    *this = ::std::move(from);
  }

  inline LatestDeviceFirmwareInfo& operator=(LatestDeviceFirmwareInfo&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }
  #endif
  static const ::google::protobuf::Descriptor* descriptor();
  static const LatestDeviceFirmwareInfo& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const LatestDeviceFirmwareInfo* internal_default_instance() {
    return reinterpret_cast<const LatestDeviceFirmwareInfo*>(
               &_LatestDeviceFirmwareInfo_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  void Swap(LatestDeviceFirmwareInfo* other);
  friend void swap(LatestDeviceFirmwareInfo& a, LatestDeviceFirmwareInfo& b) {
    a.Swap(&b);
  }

  // implements Message ----------------------------------------------

  inline LatestDeviceFirmwareInfo* New() const final {
    return CreateMaybeMessage<LatestDeviceFirmwareInfo>(NULL);
  }

  LatestDeviceFirmwareInfo* New(::google::protobuf::Arena* arena) const final {
    return CreateMaybeMessage<LatestDeviceFirmwareInfo>(arena);
  }
  void CopyFrom(const ::google::protobuf::Message& from) final;
  void MergeFrom(const ::google::protobuf::Message& from) final;
  void CopyFrom(const LatestDeviceFirmwareInfo& from);
  void MergeFrom(const LatestDeviceFirmwareInfo& from);
  void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input) final;
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const final;
  ::google::protobuf::uint8* InternalSerializeWithCachedSizesToArray(
      bool deterministic, ::google::protobuf::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(LatestDeviceFirmwareInfo* other);
  private:
  inline ::google::protobuf::Arena* GetArenaNoVirtual() const {
    return NULL;
  }
  inline void* MaybeArenaPtr() const {
    return NULL;
  }
  public:

  ::google::protobuf::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // string latest_firmware_version = 3;
  void clear_latest_firmware_version();
  static const int kLatestFirmwareVersionFieldNumber = 3;
  const ::std::string& latest_firmware_version() const;
  void set_latest_firmware_version(const ::std::string& value);
  #if LANG_CXX11
  void set_latest_firmware_version(::std::string&& value);
  #endif
  void set_latest_firmware_version(const char* value);
  void set_latest_firmware_version(const char* value, size_t size);
  ::std::string* mutable_latest_firmware_version();
  ::std::string* release_latest_firmware_version();
  void set_allocated_latest_firmware_version(::std::string* latest_firmware_version);

  // .logi.proto.Device.FormFactor device_form_factor = 1;
  void clear_device_form_factor();
  static const int kDeviceFormFactorFieldNumber = 1;
  ::logi::proto::Device_FormFactor device_form_factor() const;
  void set_device_form_factor(::logi::proto::Device_FormFactor value);

  // .logi.proto.DeviceInfo.Type type = 2;
  void clear_type();
  static const int kTypeFieldNumber = 2;
  ::logi::proto::DeviceInfo_Type type() const;
  void set_type(::logi::proto::DeviceInfo_Type value);

  // @@protoc_insertion_point(class_scope:logi.proto.LatestDeviceFirmwareInfo)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::internal::ArenaStringPtr latest_firmware_version_;
  int device_form_factor_;
  int type_;
  mutable ::google::protobuf::internal::CachedSize _cached_size_;
  friend struct ::protobuf_firmware_5fstructures_2eproto::TableStruct;
};
// -------------------------------------------------------------------

class FirmwareUpdateProgress : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:logi.proto.FirmwareUpdateProgress) */ {
 public:
  FirmwareUpdateProgress();
  virtual ~FirmwareUpdateProgress();

  FirmwareUpdateProgress(const FirmwareUpdateProgress& from);

  inline FirmwareUpdateProgress& operator=(const FirmwareUpdateProgress& from) {
    CopyFrom(from);
    return *this;
  }
  #if LANG_CXX11
  FirmwareUpdateProgress(FirmwareUpdateProgress&& from) noexcept
    : FirmwareUpdateProgress() {
    *this = ::std::move(from);
  }

  inline FirmwareUpdateProgress& operator=(FirmwareUpdateProgress&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }
  #endif
  static const ::google::protobuf::Descriptor* descriptor();
  static const FirmwareUpdateProgress& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const FirmwareUpdateProgress* internal_default_instance() {
    return reinterpret_cast<const FirmwareUpdateProgress*>(
               &_FirmwareUpdateProgress_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  void Swap(FirmwareUpdateProgress* other);
  friend void swap(FirmwareUpdateProgress& a, FirmwareUpdateProgress& b) {
    a.Swap(&b);
  }

  // implements Message ----------------------------------------------

  inline FirmwareUpdateProgress* New() const final {
    return CreateMaybeMessage<FirmwareUpdateProgress>(NULL);
  }

  FirmwareUpdateProgress* New(::google::protobuf::Arena* arena) const final {
    return CreateMaybeMessage<FirmwareUpdateProgress>(arena);
  }
  void CopyFrom(const ::google::protobuf::Message& from) final;
  void MergeFrom(const ::google::protobuf::Message& from) final;
  void CopyFrom(const FirmwareUpdateProgress& from);
  void MergeFrom(const FirmwareUpdateProgress& from);
  void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input) final;
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const final;
  ::google::protobuf::uint8* InternalSerializeWithCachedSizesToArray(
      bool deterministic, ::google::protobuf::uint8* target) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(FirmwareUpdateProgress* other);
  private:
  inline ::google::protobuf::Arena* GetArenaNoVirtual() const {
    return NULL;
  }
  inline void* MaybeArenaPtr() const {
    return NULL;
  }
  public:

  ::google::protobuf::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // string product_uuid = 1;
  void clear_product_uuid();
  static const int kProductUuidFieldNumber = 1;
  const ::std::string& product_uuid() const;
  void set_product_uuid(const ::std::string& value);
  #if LANG_CXX11
  void set_product_uuid(::std::string&& value);
  #endif
  void set_product_uuid(const char* value);
  void set_product_uuid(const char* value, size_t size);
  ::std::string* mutable_product_uuid();
  ::std::string* release_product_uuid();
  void set_allocated_product_uuid(::std::string* product_uuid);

  // string device_uuid = 2;
  void clear_device_uuid();
  static const int kDeviceUuidFieldNumber = 2;
  const ::std::string& device_uuid() const;
  void set_device_uuid(const ::std::string& value);
  #if LANG_CXX11
  void set_device_uuid(::std::string&& value);
  #endif
  void set_device_uuid(const char* value);
  void set_device_uuid(const char* value, size_t size);
  ::std::string* mutable_device_uuid();
  ::std::string* release_device_uuid();
  void set_allocated_device_uuid(::std::string* device_uuid);

  // string firmware_package_version = 3;
  void clear_firmware_package_version();
  static const int kFirmwarePackageVersionFieldNumber = 3;
  const ::std::string& firmware_package_version() const;
  void set_firmware_package_version(const ::std::string& value);
  #if LANG_CXX11
  void set_firmware_package_version(::std::string&& value);
  #endif
  void set_firmware_package_version(const char* value);
  void set_firmware_package_version(const char* value, size_t size);
  ::std::string* mutable_firmware_package_version();
  ::std::string* release_firmware_package_version();
  void set_allocated_firmware_package_version(::std::string* firmware_package_version);

  // float current_progress = 4;
  void clear_current_progress();
  static const int kCurrentProgressFieldNumber = 4;
  float current_progress() const;
  void set_current_progress(float value);

  // float overall_progress = 5;
  void clear_overall_progress();
  static const int kOverallProgressFieldNumber = 5;
  float overall_progress() const;
  void set_overall_progress(float value);

  // uint32 remaining_update_time = 6;
  void clear_remaining_update_time();
  static const int kRemainingUpdateTimeFieldNumber = 6;
  ::google::protobuf::uint32 remaining_update_time() const;
  void set_remaining_update_time(::google::protobuf::uint32 value);

  // @@protoc_insertion_point(class_scope:logi.proto.FirmwareUpdateProgress)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::internal::ArenaStringPtr product_uuid_;
  ::google::protobuf::internal::ArenaStringPtr device_uuid_;
  ::google::protobuf::internal::ArenaStringPtr firmware_package_version_;
  float current_progress_;
  float overall_progress_;
  ::google::protobuf::uint32 remaining_update_time_;
  mutable ::google::protobuf::internal::CachedSize _cached_size_;
  friend struct ::protobuf_firmware_5fstructures_2eproto::TableStruct;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// LatestDeviceFirmwareInfo

// .logi.proto.Device.FormFactor device_form_factor = 1;
inline void LatestDeviceFirmwareInfo::clear_device_form_factor() {
  device_form_factor_ = 0;
}
inline ::logi::proto::Device_FormFactor LatestDeviceFirmwareInfo::device_form_factor() const {
  // @@protoc_insertion_point(field_get:logi.proto.LatestDeviceFirmwareInfo.device_form_factor)
  return static_cast< ::logi::proto::Device_FormFactor >(device_form_factor_);
}
inline void LatestDeviceFirmwareInfo::set_device_form_factor(::logi::proto::Device_FormFactor value) {
  
  device_form_factor_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.LatestDeviceFirmwareInfo.device_form_factor)
}

// .logi.proto.DeviceInfo.Type type = 2;
inline void LatestDeviceFirmwareInfo::clear_type() {
  type_ = 0;
}
inline ::logi::proto::DeviceInfo_Type LatestDeviceFirmwareInfo::type() const {
  // @@protoc_insertion_point(field_get:logi.proto.LatestDeviceFirmwareInfo.type)
  return static_cast< ::logi::proto::DeviceInfo_Type >(type_);
}
inline void LatestDeviceFirmwareInfo::set_type(::logi::proto::DeviceInfo_Type value) {
  
  type_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.LatestDeviceFirmwareInfo.type)
}

// string latest_firmware_version = 3;
inline void LatestDeviceFirmwareInfo::clear_latest_firmware_version() {
  latest_firmware_version_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& LatestDeviceFirmwareInfo::latest_firmware_version() const {
  // @@protoc_insertion_point(field_get:logi.proto.LatestDeviceFirmwareInfo.latest_firmware_version)
  return latest_firmware_version_.GetNoArena();
}
inline void LatestDeviceFirmwareInfo::set_latest_firmware_version(const ::std::string& value) {
  
  latest_firmware_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.LatestDeviceFirmwareInfo.latest_firmware_version)
}
#if LANG_CXX11
inline void LatestDeviceFirmwareInfo::set_latest_firmware_version(::std::string&& value) {
  
  latest_firmware_version_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.LatestDeviceFirmwareInfo.latest_firmware_version)
}
#endif
inline void LatestDeviceFirmwareInfo::set_latest_firmware_version(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  latest_firmware_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.LatestDeviceFirmwareInfo.latest_firmware_version)
}
inline void LatestDeviceFirmwareInfo::set_latest_firmware_version(const char* value, size_t size) {
  
  latest_firmware_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.LatestDeviceFirmwareInfo.latest_firmware_version)
}
inline ::std::string* LatestDeviceFirmwareInfo::mutable_latest_firmware_version() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.LatestDeviceFirmwareInfo.latest_firmware_version)
  return latest_firmware_version_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* LatestDeviceFirmwareInfo::release_latest_firmware_version() {
  // @@protoc_insertion_point(field_release:logi.proto.LatestDeviceFirmwareInfo.latest_firmware_version)
  
  return latest_firmware_version_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void LatestDeviceFirmwareInfo::set_allocated_latest_firmware_version(::std::string* latest_firmware_version) {
  if (latest_firmware_version != NULL) {
    
  } else {
    
  }
  latest_firmware_version_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), latest_firmware_version);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.LatestDeviceFirmwareInfo.latest_firmware_version)
}

// -------------------------------------------------------------------

// FirmwareUpdateProgress

// string product_uuid = 1;
inline void FirmwareUpdateProgress::clear_product_uuid() {
  product_uuid_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& FirmwareUpdateProgress::product_uuid() const {
  // @@protoc_insertion_point(field_get:logi.proto.FirmwareUpdateProgress.product_uuid)
  return product_uuid_.GetNoArena();
}
inline void FirmwareUpdateProgress::set_product_uuid(const ::std::string& value) {
  
  product_uuid_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.FirmwareUpdateProgress.product_uuid)
}
#if LANG_CXX11
inline void FirmwareUpdateProgress::set_product_uuid(::std::string&& value) {
  
  product_uuid_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.FirmwareUpdateProgress.product_uuid)
}
#endif
inline void FirmwareUpdateProgress::set_product_uuid(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  product_uuid_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.FirmwareUpdateProgress.product_uuid)
}
inline void FirmwareUpdateProgress::set_product_uuid(const char* value, size_t size) {
  
  product_uuid_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.FirmwareUpdateProgress.product_uuid)
}
inline ::std::string* FirmwareUpdateProgress::mutable_product_uuid() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.FirmwareUpdateProgress.product_uuid)
  return product_uuid_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* FirmwareUpdateProgress::release_product_uuid() {
  // @@protoc_insertion_point(field_release:logi.proto.FirmwareUpdateProgress.product_uuid)
  
  return product_uuid_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void FirmwareUpdateProgress::set_allocated_product_uuid(::std::string* product_uuid) {
  if (product_uuid != NULL) {
    
  } else {
    
  }
  product_uuid_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), product_uuid);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.FirmwareUpdateProgress.product_uuid)
}

// string device_uuid = 2;
inline void FirmwareUpdateProgress::clear_device_uuid() {
  device_uuid_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& FirmwareUpdateProgress::device_uuid() const {
  // @@protoc_insertion_point(field_get:logi.proto.FirmwareUpdateProgress.device_uuid)
  return device_uuid_.GetNoArena();
}
inline void FirmwareUpdateProgress::set_device_uuid(const ::std::string& value) {
  
  device_uuid_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.FirmwareUpdateProgress.device_uuid)
}
#if LANG_CXX11
inline void FirmwareUpdateProgress::set_device_uuid(::std::string&& value) {
  
  device_uuid_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.FirmwareUpdateProgress.device_uuid)
}
#endif
inline void FirmwareUpdateProgress::set_device_uuid(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  device_uuid_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.FirmwareUpdateProgress.device_uuid)
}
inline void FirmwareUpdateProgress::set_device_uuid(const char* value, size_t size) {
  
  device_uuid_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.FirmwareUpdateProgress.device_uuid)
}
inline ::std::string* FirmwareUpdateProgress::mutable_device_uuid() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.FirmwareUpdateProgress.device_uuid)
  return device_uuid_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* FirmwareUpdateProgress::release_device_uuid() {
  // @@protoc_insertion_point(field_release:logi.proto.FirmwareUpdateProgress.device_uuid)
  
  return device_uuid_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void FirmwareUpdateProgress::set_allocated_device_uuid(::std::string* device_uuid) {
  if (device_uuid != NULL) {
    
  } else {
    
  }
  device_uuid_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), device_uuid);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.FirmwareUpdateProgress.device_uuid)
}

// string firmware_package_version = 3;
inline void FirmwareUpdateProgress::clear_firmware_package_version() {
  firmware_package_version_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& FirmwareUpdateProgress::firmware_package_version() const {
  // @@protoc_insertion_point(field_get:logi.proto.FirmwareUpdateProgress.firmware_package_version)
  return firmware_package_version_.GetNoArena();
}
inline void FirmwareUpdateProgress::set_firmware_package_version(const ::std::string& value) {
  
  firmware_package_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.FirmwareUpdateProgress.firmware_package_version)
}
#if LANG_CXX11
inline void FirmwareUpdateProgress::set_firmware_package_version(::std::string&& value) {
  
  firmware_package_version_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.FirmwareUpdateProgress.firmware_package_version)
}
#endif
inline void FirmwareUpdateProgress::set_firmware_package_version(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  firmware_package_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.FirmwareUpdateProgress.firmware_package_version)
}
inline void FirmwareUpdateProgress::set_firmware_package_version(const char* value, size_t size) {
  
  firmware_package_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.FirmwareUpdateProgress.firmware_package_version)
}
inline ::std::string* FirmwareUpdateProgress::mutable_firmware_package_version() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.FirmwareUpdateProgress.firmware_package_version)
  return firmware_package_version_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* FirmwareUpdateProgress::release_firmware_package_version() {
  // @@protoc_insertion_point(field_release:logi.proto.FirmwareUpdateProgress.firmware_package_version)
  
  return firmware_package_version_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void FirmwareUpdateProgress::set_allocated_firmware_package_version(::std::string* firmware_package_version) {
  if (firmware_package_version != NULL) {
    
  } else {
    
  }
  firmware_package_version_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), firmware_package_version);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.FirmwareUpdateProgress.firmware_package_version)
}

// float current_progress = 4;
inline void FirmwareUpdateProgress::clear_current_progress() {
  current_progress_ = 0;
}
inline float FirmwareUpdateProgress::current_progress() const {
  // @@protoc_insertion_point(field_get:logi.proto.FirmwareUpdateProgress.current_progress)
  return current_progress_;
}
inline void FirmwareUpdateProgress::set_current_progress(float value) {
  
  current_progress_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.FirmwareUpdateProgress.current_progress)
}

// float overall_progress = 5;
inline void FirmwareUpdateProgress::clear_overall_progress() {
  overall_progress_ = 0;
}
inline float FirmwareUpdateProgress::overall_progress() const {
  // @@protoc_insertion_point(field_get:logi.proto.FirmwareUpdateProgress.overall_progress)
  return overall_progress_;
}
inline void FirmwareUpdateProgress::set_overall_progress(float value) {
  
  overall_progress_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.FirmwareUpdateProgress.overall_progress)
}

// uint32 remaining_update_time = 6;
inline void FirmwareUpdateProgress::clear_remaining_update_time() {
  remaining_update_time_ = 0u;
}
inline ::google::protobuf::uint32 FirmwareUpdateProgress::remaining_update_time() const {
  // @@protoc_insertion_point(field_get:logi.proto.FirmwareUpdateProgress.remaining_update_time)
  return remaining_update_time_;
}
inline void FirmwareUpdateProgress::set_remaining_update_time(::google::protobuf::uint32 value) {
  
  remaining_update_time_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.FirmwareUpdateProgress.remaining_update_time)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace proto
}  // namespace logi

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_INCLUDED_firmware_5fstructures_2eproto

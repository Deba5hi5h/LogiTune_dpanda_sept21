// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: sync_agent_software_update_structures.proto

#ifndef PROTOBUF_INCLUDED_sync_5fagent_5fsoftware_5fupdate_5fstructures_2eproto
#define PROTOBUF_INCLUDED_sync_5fagent_5fsoftware_5fupdate_5fstructures_2eproto

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
// @@protoc_insertion_point(includes)
#define PROTOBUF_INTERNAL_EXPORT_protobuf_sync_5fagent_5fsoftware_5fupdate_5fstructures_2eproto 

namespace protobuf_sync_5fagent_5fsoftware_5fupdate_5fstructures_2eproto {
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
}  // namespace protobuf_sync_5fagent_5fsoftware_5fupdate_5fstructures_2eproto
namespace logi {
namespace proto {
class LSALastSoftwareUpdateStatus;
class LSALastSoftwareUpdateStatusDefaultTypeInternal;
extern LSALastSoftwareUpdateStatusDefaultTypeInternal _LSALastSoftwareUpdateStatus_default_instance_;
class LSASoftwareUpdateReport;
class LSASoftwareUpdateReportDefaultTypeInternal;
extern LSASoftwareUpdateReportDefaultTypeInternal _LSASoftwareUpdateReport_default_instance_;
}  // namespace proto
}  // namespace logi
namespace google {
namespace protobuf {
template<> ::logi::proto::LSALastSoftwareUpdateStatus* Arena::CreateMaybeMessage<::logi::proto::LSALastSoftwareUpdateStatus>(Arena*);
template<> ::logi::proto::LSASoftwareUpdateReport* Arena::CreateMaybeMessage<::logi::proto::LSASoftwareUpdateReport>(Arena*);
}  // namespace protobuf
}  // namespace google
namespace logi {
namespace proto {

// ===================================================================

class LSASoftwareUpdateReport : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:logi.proto.LSASoftwareUpdateReport) */ {
 public:
  LSASoftwareUpdateReport();
  virtual ~LSASoftwareUpdateReport();

  LSASoftwareUpdateReport(const LSASoftwareUpdateReport& from);

  inline LSASoftwareUpdateReport& operator=(const LSASoftwareUpdateReport& from) {
    CopyFrom(from);
    return *this;
  }
  #if LANG_CXX11
  LSASoftwareUpdateReport(LSASoftwareUpdateReport&& from) noexcept
    : LSASoftwareUpdateReport() {
    *this = ::std::move(from);
  }

  inline LSASoftwareUpdateReport& operator=(LSASoftwareUpdateReport&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }
  #endif
  static const ::google::protobuf::Descriptor* descriptor();
  static const LSASoftwareUpdateReport& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const LSASoftwareUpdateReport* internal_default_instance() {
    return reinterpret_cast<const LSASoftwareUpdateReport*>(
               &_LSASoftwareUpdateReport_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  void Swap(LSASoftwareUpdateReport* other);
  friend void swap(LSASoftwareUpdateReport& a, LSASoftwareUpdateReport& b) {
    a.Swap(&b);
  }

  // implements Message ----------------------------------------------

  inline LSASoftwareUpdateReport* New() const final {
    return CreateMaybeMessage<LSASoftwareUpdateReport>(NULL);
  }

  LSASoftwareUpdateReport* New(::google::protobuf::Arena* arena) const final {
    return CreateMaybeMessage<LSASoftwareUpdateReport>(arena);
  }
  void CopyFrom(const ::google::protobuf::Message& from) final;
  void MergeFrom(const ::google::protobuf::Message& from) final;
  void CopyFrom(const LSASoftwareUpdateReport& from);
  void MergeFrom(const LSASoftwareUpdateReport& from);
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
  void InternalSwap(LSASoftwareUpdateReport* other);
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

  // string current_software_package_version = 2;
  void clear_current_software_package_version();
  static const int kCurrentSoftwarePackageVersionFieldNumber = 2;
  const ::std::string& current_software_package_version() const;
  void set_current_software_package_version(const ::std::string& value);
  #if LANG_CXX11
  void set_current_software_package_version(::std::string&& value);
  #endif
  void set_current_software_package_version(const char* value);
  void set_current_software_package_version(const char* value, size_t size);
  ::std::string* mutable_current_software_package_version();
  ::std::string* release_current_software_package_version();
  void set_allocated_current_software_package_version(::std::string* current_software_package_version);

  // string target_software_package_version = 3;
  void clear_target_software_package_version();
  static const int kTargetSoftwarePackageVersionFieldNumber = 3;
  const ::std::string& target_software_package_version() const;
  void set_target_software_package_version(const ::std::string& value);
  #if LANG_CXX11
  void set_target_software_package_version(::std::string&& value);
  #endif
  void set_target_software_package_version(const char* value);
  void set_target_software_package_version(const char* value, size_t size);
  ::std::string* mutable_target_software_package_version();
  ::std::string* release_target_software_package_version();
  void set_allocated_target_software_package_version(::std::string* target_software_package_version);

  // .logi.proto.LSALastSoftwareUpdateStatus last_update_status = 4;
  bool has_last_update_status() const;
  void clear_last_update_status();
  static const int kLastUpdateStatusFieldNumber = 4;
  private:
  const ::logi::proto::LSALastSoftwareUpdateStatus& _internal_last_update_status() const;
  public:
  const ::logi::proto::LSALastSoftwareUpdateStatus& last_update_status() const;
  ::logi::proto::LSALastSoftwareUpdateStatus* release_last_update_status();
  ::logi::proto::LSALastSoftwareUpdateStatus* mutable_last_update_status();
  void set_allocated_last_update_status(::logi::proto::LSALastSoftwareUpdateStatus* last_update_status);

  // .logi.proto.SyncUpdateState update_state = 1;
  void clear_update_state();
  static const int kUpdateStateFieldNumber = 1;
  ::logi::proto::SyncUpdateState update_state() const;
  void set_update_state(::logi::proto::SyncUpdateState value);

  // @@protoc_insertion_point(class_scope:logi.proto.LSASoftwareUpdateReport)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::internal::ArenaStringPtr current_software_package_version_;
  ::google::protobuf::internal::ArenaStringPtr target_software_package_version_;
  ::logi::proto::LSALastSoftwareUpdateStatus* last_update_status_;
  int update_state_;
  mutable ::google::protobuf::internal::CachedSize _cached_size_;
  friend struct ::protobuf_sync_5fagent_5fsoftware_5fupdate_5fstructures_2eproto::TableStruct;
};
// -------------------------------------------------------------------

class LSALastSoftwareUpdateStatus : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:logi.proto.LSALastSoftwareUpdateStatus) */ {
 public:
  LSALastSoftwareUpdateStatus();
  virtual ~LSALastSoftwareUpdateStatus();

  LSALastSoftwareUpdateStatus(const LSALastSoftwareUpdateStatus& from);

  inline LSALastSoftwareUpdateStatus& operator=(const LSALastSoftwareUpdateStatus& from) {
    CopyFrom(from);
    return *this;
  }
  #if LANG_CXX11
  LSALastSoftwareUpdateStatus(LSALastSoftwareUpdateStatus&& from) noexcept
    : LSALastSoftwareUpdateStatus() {
    *this = ::std::move(from);
  }

  inline LSALastSoftwareUpdateStatus& operator=(LSALastSoftwareUpdateStatus&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }
  #endif
  static const ::google::protobuf::Descriptor* descriptor();
  static const LSALastSoftwareUpdateStatus& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const LSALastSoftwareUpdateStatus* internal_default_instance() {
    return reinterpret_cast<const LSALastSoftwareUpdateStatus*>(
               &_LSALastSoftwareUpdateStatus_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  void Swap(LSALastSoftwareUpdateStatus* other);
  friend void swap(LSALastSoftwareUpdateStatus& a, LSALastSoftwareUpdateStatus& b) {
    a.Swap(&b);
  }

  // implements Message ----------------------------------------------

  inline LSALastSoftwareUpdateStatus* New() const final {
    return CreateMaybeMessage<LSALastSoftwareUpdateStatus>(NULL);
  }

  LSALastSoftwareUpdateStatus* New(::google::protobuf::Arena* arena) const final {
    return CreateMaybeMessage<LSALastSoftwareUpdateStatus>(arena);
  }
  void CopyFrom(const ::google::protobuf::Message& from) final;
  void MergeFrom(const ::google::protobuf::Message& from) final;
  void CopyFrom(const LSALastSoftwareUpdateStatus& from);
  void MergeFrom(const LSALastSoftwareUpdateStatus& from);
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
  void InternalSwap(LSALastSoftwareUpdateStatus* other);
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

  // repeated .logi.proto.Error update_errors = 2;
  int update_errors_size() const;
  void clear_update_errors();
  static const int kUpdateErrorsFieldNumber = 2;
  ::logi::proto::Error* mutable_update_errors(int index);
  ::google::protobuf::RepeatedPtrField< ::logi::proto::Error >*
      mutable_update_errors();
  const ::logi::proto::Error& update_errors(int index) const;
  ::logi::proto::Error* add_update_errors();
  const ::google::protobuf::RepeatedPtrField< ::logi::proto::Error >&
      update_errors() const;

  // bool update_failed = 1;
  void clear_update_failed();
  static const int kUpdateFailedFieldNumber = 1;
  bool update_failed() const;
  void set_update_failed(bool value);

  // @@protoc_insertion_point(class_scope:logi.proto.LSALastSoftwareUpdateStatus)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::RepeatedPtrField< ::logi::proto::Error > update_errors_;
  bool update_failed_;
  mutable ::google::protobuf::internal::CachedSize _cached_size_;
  friend struct ::protobuf_sync_5fagent_5fsoftware_5fupdate_5fstructures_2eproto::TableStruct;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// LSASoftwareUpdateReport

// .logi.proto.SyncUpdateState update_state = 1;
inline void LSASoftwareUpdateReport::clear_update_state() {
  update_state_ = 0;
}
inline ::logi::proto::SyncUpdateState LSASoftwareUpdateReport::update_state() const {
  // @@protoc_insertion_point(field_get:logi.proto.LSASoftwareUpdateReport.update_state)
  return static_cast< ::logi::proto::SyncUpdateState >(update_state_);
}
inline void LSASoftwareUpdateReport::set_update_state(::logi::proto::SyncUpdateState value) {
  
  update_state_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.LSASoftwareUpdateReport.update_state)
}

// string current_software_package_version = 2;
inline void LSASoftwareUpdateReport::clear_current_software_package_version() {
  current_software_package_version_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& LSASoftwareUpdateReport::current_software_package_version() const {
  // @@protoc_insertion_point(field_get:logi.proto.LSASoftwareUpdateReport.current_software_package_version)
  return current_software_package_version_.GetNoArena();
}
inline void LSASoftwareUpdateReport::set_current_software_package_version(const ::std::string& value) {
  
  current_software_package_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.LSASoftwareUpdateReport.current_software_package_version)
}
#if LANG_CXX11
inline void LSASoftwareUpdateReport::set_current_software_package_version(::std::string&& value) {
  
  current_software_package_version_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.LSASoftwareUpdateReport.current_software_package_version)
}
#endif
inline void LSASoftwareUpdateReport::set_current_software_package_version(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  current_software_package_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.LSASoftwareUpdateReport.current_software_package_version)
}
inline void LSASoftwareUpdateReport::set_current_software_package_version(const char* value, size_t size) {
  
  current_software_package_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.LSASoftwareUpdateReport.current_software_package_version)
}
inline ::std::string* LSASoftwareUpdateReport::mutable_current_software_package_version() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.LSASoftwareUpdateReport.current_software_package_version)
  return current_software_package_version_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* LSASoftwareUpdateReport::release_current_software_package_version() {
  // @@protoc_insertion_point(field_release:logi.proto.LSASoftwareUpdateReport.current_software_package_version)
  
  return current_software_package_version_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void LSASoftwareUpdateReport::set_allocated_current_software_package_version(::std::string* current_software_package_version) {
  if (current_software_package_version != NULL) {
    
  } else {
    
  }
  current_software_package_version_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), current_software_package_version);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.LSASoftwareUpdateReport.current_software_package_version)
}

// string target_software_package_version = 3;
inline void LSASoftwareUpdateReport::clear_target_software_package_version() {
  target_software_package_version_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& LSASoftwareUpdateReport::target_software_package_version() const {
  // @@protoc_insertion_point(field_get:logi.proto.LSASoftwareUpdateReport.target_software_package_version)
  return target_software_package_version_.GetNoArena();
}
inline void LSASoftwareUpdateReport::set_target_software_package_version(const ::std::string& value) {
  
  target_software_package_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.LSASoftwareUpdateReport.target_software_package_version)
}
#if LANG_CXX11
inline void LSASoftwareUpdateReport::set_target_software_package_version(::std::string&& value) {
  
  target_software_package_version_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.LSASoftwareUpdateReport.target_software_package_version)
}
#endif
inline void LSASoftwareUpdateReport::set_target_software_package_version(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  target_software_package_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.LSASoftwareUpdateReport.target_software_package_version)
}
inline void LSASoftwareUpdateReport::set_target_software_package_version(const char* value, size_t size) {
  
  target_software_package_version_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.LSASoftwareUpdateReport.target_software_package_version)
}
inline ::std::string* LSASoftwareUpdateReport::mutable_target_software_package_version() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.LSASoftwareUpdateReport.target_software_package_version)
  return target_software_package_version_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* LSASoftwareUpdateReport::release_target_software_package_version() {
  // @@protoc_insertion_point(field_release:logi.proto.LSASoftwareUpdateReport.target_software_package_version)
  
  return target_software_package_version_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void LSASoftwareUpdateReport::set_allocated_target_software_package_version(::std::string* target_software_package_version) {
  if (target_software_package_version != NULL) {
    
  } else {
    
  }
  target_software_package_version_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), target_software_package_version);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.LSASoftwareUpdateReport.target_software_package_version)
}

// .logi.proto.LSALastSoftwareUpdateStatus last_update_status = 4;
inline bool LSASoftwareUpdateReport::has_last_update_status() const {
  return this != internal_default_instance() && last_update_status_ != NULL;
}
inline void LSASoftwareUpdateReport::clear_last_update_status() {
  if (GetArenaNoVirtual() == NULL && last_update_status_ != NULL) {
    delete last_update_status_;
  }
  last_update_status_ = NULL;
}
inline const ::logi::proto::LSALastSoftwareUpdateStatus& LSASoftwareUpdateReport::_internal_last_update_status() const {
  return *last_update_status_;
}
inline const ::logi::proto::LSALastSoftwareUpdateStatus& LSASoftwareUpdateReport::last_update_status() const {
  const ::logi::proto::LSALastSoftwareUpdateStatus* p = last_update_status_;
  // @@protoc_insertion_point(field_get:logi.proto.LSASoftwareUpdateReport.last_update_status)
  return p != NULL ? *p : *reinterpret_cast<const ::logi::proto::LSALastSoftwareUpdateStatus*>(
      &::logi::proto::_LSALastSoftwareUpdateStatus_default_instance_);
}
inline ::logi::proto::LSALastSoftwareUpdateStatus* LSASoftwareUpdateReport::release_last_update_status() {
  // @@protoc_insertion_point(field_release:logi.proto.LSASoftwareUpdateReport.last_update_status)
  
  ::logi::proto::LSALastSoftwareUpdateStatus* temp = last_update_status_;
  last_update_status_ = NULL;
  return temp;
}
inline ::logi::proto::LSALastSoftwareUpdateStatus* LSASoftwareUpdateReport::mutable_last_update_status() {
  
  if (last_update_status_ == NULL) {
    auto* p = CreateMaybeMessage<::logi::proto::LSALastSoftwareUpdateStatus>(GetArenaNoVirtual());
    last_update_status_ = p;
  }
  // @@protoc_insertion_point(field_mutable:logi.proto.LSASoftwareUpdateReport.last_update_status)
  return last_update_status_;
}
inline void LSASoftwareUpdateReport::set_allocated_last_update_status(::logi::proto::LSALastSoftwareUpdateStatus* last_update_status) {
  ::google::protobuf::Arena* message_arena = GetArenaNoVirtual();
  if (message_arena == NULL) {
    delete last_update_status_;
  }
  if (last_update_status) {
    ::google::protobuf::Arena* submessage_arena = NULL;
    if (message_arena != submessage_arena) {
      last_update_status = ::google::protobuf::internal::GetOwnedMessage(
          message_arena, last_update_status, submessage_arena);
    }
    
  } else {
    
  }
  last_update_status_ = last_update_status;
  // @@protoc_insertion_point(field_set_allocated:logi.proto.LSASoftwareUpdateReport.last_update_status)
}

// -------------------------------------------------------------------

// LSALastSoftwareUpdateStatus

// bool update_failed = 1;
inline void LSALastSoftwareUpdateStatus::clear_update_failed() {
  update_failed_ = false;
}
inline bool LSALastSoftwareUpdateStatus::update_failed() const {
  // @@protoc_insertion_point(field_get:logi.proto.LSALastSoftwareUpdateStatus.update_failed)
  return update_failed_;
}
inline void LSALastSoftwareUpdateStatus::set_update_failed(bool value) {
  
  update_failed_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.LSALastSoftwareUpdateStatus.update_failed)
}

// repeated .logi.proto.Error update_errors = 2;
inline int LSALastSoftwareUpdateStatus::update_errors_size() const {
  return update_errors_.size();
}
inline ::logi::proto::Error* LSALastSoftwareUpdateStatus::mutable_update_errors(int index) {
  // @@protoc_insertion_point(field_mutable:logi.proto.LSALastSoftwareUpdateStatus.update_errors)
  return update_errors_.Mutable(index);
}
inline ::google::protobuf::RepeatedPtrField< ::logi::proto::Error >*
LSALastSoftwareUpdateStatus::mutable_update_errors() {
  // @@protoc_insertion_point(field_mutable_list:logi.proto.LSALastSoftwareUpdateStatus.update_errors)
  return &update_errors_;
}
inline const ::logi::proto::Error& LSALastSoftwareUpdateStatus::update_errors(int index) const {
  // @@protoc_insertion_point(field_get:logi.proto.LSALastSoftwareUpdateStatus.update_errors)
  return update_errors_.Get(index);
}
inline ::logi::proto::Error* LSALastSoftwareUpdateStatus::add_update_errors() {
  // @@protoc_insertion_point(field_add:logi.proto.LSALastSoftwareUpdateStatus.update_errors)
  return update_errors_.Add();
}
inline const ::google::protobuf::RepeatedPtrField< ::logi::proto::Error >&
LSALastSoftwareUpdateStatus::update_errors() const {
  // @@protoc_insertion_point(field_list:logi.proto.LSALastSoftwareUpdateStatus.update_errors)
  return update_errors_;
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace proto
}  // namespace logi

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_INCLUDED_sync_5fagent_5fsoftware_5fupdate_5fstructures_2eproto

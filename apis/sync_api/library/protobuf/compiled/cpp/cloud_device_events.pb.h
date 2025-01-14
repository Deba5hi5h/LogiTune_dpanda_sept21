// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: cloud_device_events.proto

#ifndef PROTOBUF_INCLUDED_cloud_5fdevice_5fevents_2eproto
#define PROTOBUF_INCLUDED_cloud_5fdevice_5fevents_2eproto

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
#include "cloud_device_structures.pb.h"
// @@protoc_insertion_point(includes)
#define PROTOBUF_INTERNAL_EXPORT_protobuf_cloud_5fdevice_5fevents_2eproto 

namespace protobuf_cloud_5fdevice_5fevents_2eproto {
// Internal implementation detail -- do not use these members.
struct TableStruct {
  static const ::google::protobuf::internal::ParseTableField entries[];
  static const ::google::protobuf::internal::AuxillaryParseTableField aux[];
  static const ::google::protobuf::internal::ParseTable schema[1];
  static const ::google::protobuf::internal::FieldMetadata field_metadata[];
  static const ::google::protobuf::internal::SerializationTable serialization_table[];
  static const ::google::protobuf::uint32 offsets[];
};
void AddDescriptors();
}  // namespace protobuf_cloud_5fdevice_5fevents_2eproto
namespace logi {
namespace proto {
class LRProductUpdatedEvent;
class LRProductUpdatedEventDefaultTypeInternal;
extern LRProductUpdatedEventDefaultTypeInternal _LRProductUpdatedEvent_default_instance_;
}  // namespace proto
}  // namespace logi
namespace google {
namespace protobuf {
template<> ::logi::proto::LRProductUpdatedEvent* Arena::CreateMaybeMessage<::logi::proto::LRProductUpdatedEvent>(Arena*);
}  // namespace protobuf
}  // namespace google
namespace logi {
namespace proto {

// ===================================================================

class LRProductUpdatedEvent : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:logi.proto.LRProductUpdatedEvent) */ {
 public:
  LRProductUpdatedEvent();
  virtual ~LRProductUpdatedEvent();

  LRProductUpdatedEvent(const LRProductUpdatedEvent& from);

  inline LRProductUpdatedEvent& operator=(const LRProductUpdatedEvent& from) {
    CopyFrom(from);
    return *this;
  }
  #if LANG_CXX11
  LRProductUpdatedEvent(LRProductUpdatedEvent&& from) noexcept
    : LRProductUpdatedEvent() {
    *this = ::std::move(from);
  }

  inline LRProductUpdatedEvent& operator=(LRProductUpdatedEvent&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }
  #endif
  static const ::google::protobuf::Descriptor* descriptor();
  static const LRProductUpdatedEvent& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const LRProductUpdatedEvent* internal_default_instance() {
    return reinterpret_cast<const LRProductUpdatedEvent*>(
               &_LRProductUpdatedEvent_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  void Swap(LRProductUpdatedEvent* other);
  friend void swap(LRProductUpdatedEvent& a, LRProductUpdatedEvent& b) {
    a.Swap(&b);
  }

  // implements Message ----------------------------------------------

  inline LRProductUpdatedEvent* New() const final {
    return CreateMaybeMessage<LRProductUpdatedEvent>(NULL);
  }

  LRProductUpdatedEvent* New(::google::protobuf::Arena* arena) const final {
    return CreateMaybeMessage<LRProductUpdatedEvent>(arena);
  }
  void CopyFrom(const ::google::protobuf::Message& from) final;
  void MergeFrom(const ::google::protobuf::Message& from) final;
  void CopyFrom(const LRProductUpdatedEvent& from);
  void MergeFrom(const LRProductUpdatedEvent& from);
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
  void InternalSwap(LRProductUpdatedEvent* other);
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

  // repeated .logi.proto.LRProductSnapshot snapshots = 5;
  int snapshots_size() const;
  void clear_snapshots();
  static const int kSnapshotsFieldNumber = 5;
  ::logi::proto::LRProductSnapshot* mutable_snapshots(int index);
  ::google::protobuf::RepeatedPtrField< ::logi::proto::LRProductSnapshot >*
      mutable_snapshots();
  const ::logi::proto::LRProductSnapshot& snapshots(int index) const;
  ::logi::proto::LRProductSnapshot* add_snapshots();
  const ::google::protobuf::RepeatedPtrField< ::logi::proto::LRProductSnapshot >&
      snapshots() const;

  // string org_info_timestamp = 1;
  void clear_org_info_timestamp();
  static const int kOrgInfoTimestampFieldNumber = 1;
  const ::std::string& org_info_timestamp() const;
  void set_org_info_timestamp(const ::std::string& value);
  #if LANG_CXX11
  void set_org_info_timestamp(::std::string&& value);
  #endif
  void set_org_info_timestamp(const char* value);
  void set_org_info_timestamp(const char* value, size_t size);
  ::std::string* mutable_org_info_timestamp();
  ::std::string* release_org_info_timestamp();
  void set_allocated_org_info_timestamp(::std::string* org_info_timestamp);

  // string org_policy_timestamp = 2;
  void clear_org_policy_timestamp();
  static const int kOrgPolicyTimestampFieldNumber = 2;
  const ::std::string& org_policy_timestamp() const;
  void set_org_policy_timestamp(const ::std::string& value);
  #if LANG_CXX11
  void set_org_policy_timestamp(::std::string&& value);
  #endif
  void set_org_policy_timestamp(const char* value);
  void set_org_policy_timestamp(const char* value, size_t size);
  ::std::string* mutable_org_policy_timestamp();
  ::std::string* release_org_policy_timestamp();
  void set_allocated_org_policy_timestamp(::std::string* org_policy_timestamp);

  // string room_info_timestamp = 3;
  void clear_room_info_timestamp();
  static const int kRoomInfoTimestampFieldNumber = 3;
  const ::std::string& room_info_timestamp() const;
  void set_room_info_timestamp(const ::std::string& value);
  #if LANG_CXX11
  void set_room_info_timestamp(::std::string&& value);
  #endif
  void set_room_info_timestamp(const char* value);
  void set_room_info_timestamp(const char* value, size_t size);
  ::std::string* mutable_room_info_timestamp();
  ::std::string* release_room_info_timestamp();
  void set_allocated_room_info_timestamp(::std::string* room_info_timestamp);

  // string room_policy_timestamp = 4;
  void clear_room_policy_timestamp();
  static const int kRoomPolicyTimestampFieldNumber = 4;
  const ::std::string& room_policy_timestamp() const;
  void set_room_policy_timestamp(const ::std::string& value);
  #if LANG_CXX11
  void set_room_policy_timestamp(::std::string&& value);
  #endif
  void set_room_policy_timestamp(const char* value);
  void set_room_policy_timestamp(const char* value, size_t size);
  ::std::string* mutable_room_policy_timestamp();
  ::std::string* release_room_policy_timestamp();
  void set_allocated_room_policy_timestamp(::std::string* room_policy_timestamp);

  // @@protoc_insertion_point(class_scope:logi.proto.LRProductUpdatedEvent)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::RepeatedPtrField< ::logi::proto::LRProductSnapshot > snapshots_;
  ::google::protobuf::internal::ArenaStringPtr org_info_timestamp_;
  ::google::protobuf::internal::ArenaStringPtr org_policy_timestamp_;
  ::google::protobuf::internal::ArenaStringPtr room_info_timestamp_;
  ::google::protobuf::internal::ArenaStringPtr room_policy_timestamp_;
  mutable ::google::protobuf::internal::CachedSize _cached_size_;
  friend struct ::protobuf_cloud_5fdevice_5fevents_2eproto::TableStruct;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// LRProductUpdatedEvent

// string org_info_timestamp = 1;
inline void LRProductUpdatedEvent::clear_org_info_timestamp() {
  org_info_timestamp_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& LRProductUpdatedEvent::org_info_timestamp() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRProductUpdatedEvent.org_info_timestamp)
  return org_info_timestamp_.GetNoArena();
}
inline void LRProductUpdatedEvent::set_org_info_timestamp(const ::std::string& value) {
  
  org_info_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.LRProductUpdatedEvent.org_info_timestamp)
}
#if LANG_CXX11
inline void LRProductUpdatedEvent::set_org_info_timestamp(::std::string&& value) {
  
  org_info_timestamp_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.LRProductUpdatedEvent.org_info_timestamp)
}
#endif
inline void LRProductUpdatedEvent::set_org_info_timestamp(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  org_info_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.LRProductUpdatedEvent.org_info_timestamp)
}
inline void LRProductUpdatedEvent::set_org_info_timestamp(const char* value, size_t size) {
  
  org_info_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.LRProductUpdatedEvent.org_info_timestamp)
}
inline ::std::string* LRProductUpdatedEvent::mutable_org_info_timestamp() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.LRProductUpdatedEvent.org_info_timestamp)
  return org_info_timestamp_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* LRProductUpdatedEvent::release_org_info_timestamp() {
  // @@protoc_insertion_point(field_release:logi.proto.LRProductUpdatedEvent.org_info_timestamp)
  
  return org_info_timestamp_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void LRProductUpdatedEvent::set_allocated_org_info_timestamp(::std::string* org_info_timestamp) {
  if (org_info_timestamp != NULL) {
    
  } else {
    
  }
  org_info_timestamp_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), org_info_timestamp);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.LRProductUpdatedEvent.org_info_timestamp)
}

// string org_policy_timestamp = 2;
inline void LRProductUpdatedEvent::clear_org_policy_timestamp() {
  org_policy_timestamp_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& LRProductUpdatedEvent::org_policy_timestamp() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRProductUpdatedEvent.org_policy_timestamp)
  return org_policy_timestamp_.GetNoArena();
}
inline void LRProductUpdatedEvent::set_org_policy_timestamp(const ::std::string& value) {
  
  org_policy_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.LRProductUpdatedEvent.org_policy_timestamp)
}
#if LANG_CXX11
inline void LRProductUpdatedEvent::set_org_policy_timestamp(::std::string&& value) {
  
  org_policy_timestamp_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.LRProductUpdatedEvent.org_policy_timestamp)
}
#endif
inline void LRProductUpdatedEvent::set_org_policy_timestamp(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  org_policy_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.LRProductUpdatedEvent.org_policy_timestamp)
}
inline void LRProductUpdatedEvent::set_org_policy_timestamp(const char* value, size_t size) {
  
  org_policy_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.LRProductUpdatedEvent.org_policy_timestamp)
}
inline ::std::string* LRProductUpdatedEvent::mutable_org_policy_timestamp() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.LRProductUpdatedEvent.org_policy_timestamp)
  return org_policy_timestamp_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* LRProductUpdatedEvent::release_org_policy_timestamp() {
  // @@protoc_insertion_point(field_release:logi.proto.LRProductUpdatedEvent.org_policy_timestamp)
  
  return org_policy_timestamp_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void LRProductUpdatedEvent::set_allocated_org_policy_timestamp(::std::string* org_policy_timestamp) {
  if (org_policy_timestamp != NULL) {
    
  } else {
    
  }
  org_policy_timestamp_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), org_policy_timestamp);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.LRProductUpdatedEvent.org_policy_timestamp)
}

// string room_info_timestamp = 3;
inline void LRProductUpdatedEvent::clear_room_info_timestamp() {
  room_info_timestamp_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& LRProductUpdatedEvent::room_info_timestamp() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRProductUpdatedEvent.room_info_timestamp)
  return room_info_timestamp_.GetNoArena();
}
inline void LRProductUpdatedEvent::set_room_info_timestamp(const ::std::string& value) {
  
  room_info_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.LRProductUpdatedEvent.room_info_timestamp)
}
#if LANG_CXX11
inline void LRProductUpdatedEvent::set_room_info_timestamp(::std::string&& value) {
  
  room_info_timestamp_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.LRProductUpdatedEvent.room_info_timestamp)
}
#endif
inline void LRProductUpdatedEvent::set_room_info_timestamp(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  room_info_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.LRProductUpdatedEvent.room_info_timestamp)
}
inline void LRProductUpdatedEvent::set_room_info_timestamp(const char* value, size_t size) {
  
  room_info_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.LRProductUpdatedEvent.room_info_timestamp)
}
inline ::std::string* LRProductUpdatedEvent::mutable_room_info_timestamp() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.LRProductUpdatedEvent.room_info_timestamp)
  return room_info_timestamp_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* LRProductUpdatedEvent::release_room_info_timestamp() {
  // @@protoc_insertion_point(field_release:logi.proto.LRProductUpdatedEvent.room_info_timestamp)
  
  return room_info_timestamp_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void LRProductUpdatedEvent::set_allocated_room_info_timestamp(::std::string* room_info_timestamp) {
  if (room_info_timestamp != NULL) {
    
  } else {
    
  }
  room_info_timestamp_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), room_info_timestamp);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.LRProductUpdatedEvent.room_info_timestamp)
}

// string room_policy_timestamp = 4;
inline void LRProductUpdatedEvent::clear_room_policy_timestamp() {
  room_policy_timestamp_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& LRProductUpdatedEvent::room_policy_timestamp() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRProductUpdatedEvent.room_policy_timestamp)
  return room_policy_timestamp_.GetNoArena();
}
inline void LRProductUpdatedEvent::set_room_policy_timestamp(const ::std::string& value) {
  
  room_policy_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.LRProductUpdatedEvent.room_policy_timestamp)
}
#if LANG_CXX11
inline void LRProductUpdatedEvent::set_room_policy_timestamp(::std::string&& value) {
  
  room_policy_timestamp_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.LRProductUpdatedEvent.room_policy_timestamp)
}
#endif
inline void LRProductUpdatedEvent::set_room_policy_timestamp(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  room_policy_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.LRProductUpdatedEvent.room_policy_timestamp)
}
inline void LRProductUpdatedEvent::set_room_policy_timestamp(const char* value, size_t size) {
  
  room_policy_timestamp_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.LRProductUpdatedEvent.room_policy_timestamp)
}
inline ::std::string* LRProductUpdatedEvent::mutable_room_policy_timestamp() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.LRProductUpdatedEvent.room_policy_timestamp)
  return room_policy_timestamp_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* LRProductUpdatedEvent::release_room_policy_timestamp() {
  // @@protoc_insertion_point(field_release:logi.proto.LRProductUpdatedEvent.room_policy_timestamp)
  
  return room_policy_timestamp_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void LRProductUpdatedEvent::set_allocated_room_policy_timestamp(::std::string* room_policy_timestamp) {
  if (room_policy_timestamp != NULL) {
    
  } else {
    
  }
  room_policy_timestamp_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), room_policy_timestamp);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.LRProductUpdatedEvent.room_policy_timestamp)
}

// repeated .logi.proto.LRProductSnapshot snapshots = 5;
inline int LRProductUpdatedEvent::snapshots_size() const {
  return snapshots_.size();
}
inline ::logi::proto::LRProductSnapshot* LRProductUpdatedEvent::mutable_snapshots(int index) {
  // @@protoc_insertion_point(field_mutable:logi.proto.LRProductUpdatedEvent.snapshots)
  return snapshots_.Mutable(index);
}
inline ::google::protobuf::RepeatedPtrField< ::logi::proto::LRProductSnapshot >*
LRProductUpdatedEvent::mutable_snapshots() {
  // @@protoc_insertion_point(field_mutable_list:logi.proto.LRProductUpdatedEvent.snapshots)
  return &snapshots_;
}
inline const ::logi::proto::LRProductSnapshot& LRProductUpdatedEvent::snapshots(int index) const {
  // @@protoc_insertion_point(field_get:logi.proto.LRProductUpdatedEvent.snapshots)
  return snapshots_.Get(index);
}
inline ::logi::proto::LRProductSnapshot* LRProductUpdatedEvent::add_snapshots() {
  // @@protoc_insertion_point(field_add:logi.proto.LRProductUpdatedEvent.snapshots)
  return snapshots_.Add();
}
inline const ::google::protobuf::RepeatedPtrField< ::logi::proto::LRProductSnapshot >&
LRProductUpdatedEvent::snapshots() const {
  // @@protoc_insertion_point(field_list:logi.proto.LRProductUpdatedEvent.snapshots)
  return snapshots_;
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace proto
}  // namespace logi

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_INCLUDED_cloud_5fdevice_5fevents_2eproto

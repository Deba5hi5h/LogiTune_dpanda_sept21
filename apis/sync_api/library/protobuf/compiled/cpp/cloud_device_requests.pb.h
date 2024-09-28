// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: cloud_device_requests.proto

#ifndef PROTOBUF_INCLUDED_cloud_5fdevice_5frequests_2eproto
#define PROTOBUF_INCLUDED_cloud_5fdevice_5frequests_2eproto

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
#define PROTOBUF_INTERNAL_EXPORT_protobuf_cloud_5fdevice_5frequests_2eproto 

namespace protobuf_cloud_5fdevice_5frequests_2eproto {
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
}  // namespace protobuf_cloud_5fdevice_5frequests_2eproto
namespace logi {
namespace proto {
class LRCheckForProductUpdateRequest;
class LRCheckForProductUpdateRequestDefaultTypeInternal;
extern LRCheckForProductUpdateRequestDefaultTypeInternal _LRCheckForProductUpdateRequest_default_instance_;
class LRCheckForProductUpdateResponse;
class LRCheckForProductUpdateResponseDefaultTypeInternal;
extern LRCheckForProductUpdateResponseDefaultTypeInternal _LRCheckForProductUpdateResponse_default_instance_;
}  // namespace proto
}  // namespace logi
namespace google {
namespace protobuf {
template<> ::logi::proto::LRCheckForProductUpdateRequest* Arena::CreateMaybeMessage<::logi::proto::LRCheckForProductUpdateRequest>(Arena*);
template<> ::logi::proto::LRCheckForProductUpdateResponse* Arena::CreateMaybeMessage<::logi::proto::LRCheckForProductUpdateResponse>(Arena*);
}  // namespace protobuf
}  // namespace google
namespace logi {
namespace proto {

// ===================================================================

class LRCheckForProductUpdateRequest : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:logi.proto.LRCheckForProductUpdateRequest) */ {
 public:
  LRCheckForProductUpdateRequest();
  virtual ~LRCheckForProductUpdateRequest();

  LRCheckForProductUpdateRequest(const LRCheckForProductUpdateRequest& from);

  inline LRCheckForProductUpdateRequest& operator=(const LRCheckForProductUpdateRequest& from) {
    CopyFrom(from);
    return *this;
  }
  #if LANG_CXX11
  LRCheckForProductUpdateRequest(LRCheckForProductUpdateRequest&& from) noexcept
    : LRCheckForProductUpdateRequest() {
    *this = ::std::move(from);
  }

  inline LRCheckForProductUpdateRequest& operator=(LRCheckForProductUpdateRequest&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }
  #endif
  static const ::google::protobuf::Descriptor* descriptor();
  static const LRCheckForProductUpdateRequest& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const LRCheckForProductUpdateRequest* internal_default_instance() {
    return reinterpret_cast<const LRCheckForProductUpdateRequest*>(
               &_LRCheckForProductUpdateRequest_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  void Swap(LRCheckForProductUpdateRequest* other);
  friend void swap(LRCheckForProductUpdateRequest& a, LRCheckForProductUpdateRequest& b) {
    a.Swap(&b);
  }

  // implements Message ----------------------------------------------

  inline LRCheckForProductUpdateRequest* New() const final {
    return CreateMaybeMessage<LRCheckForProductUpdateRequest>(NULL);
  }

  LRCheckForProductUpdateRequest* New(::google::protobuf::Arena* arena) const final {
    return CreateMaybeMessage<LRCheckForProductUpdateRequest>(arena);
  }
  void CopyFrom(const ::google::protobuf::Message& from) final;
  void MergeFrom(const ::google::protobuf::Message& from) final;
  void CopyFrom(const LRCheckForProductUpdateRequest& from);
  void MergeFrom(const LRCheckForProductUpdateRequest& from);
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
  void InternalSwap(LRCheckForProductUpdateRequest* other);
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

  // string product_uuid = 2;
  void clear_product_uuid();
  static const int kProductUuidFieldNumber = 2;
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

  // bool update_now = 1;
  void clear_update_now();
  static const int kUpdateNowFieldNumber = 1;
  bool update_now() const;
  void set_update_now(bool value);

  // .logi.proto.Product.Model product_model = 3;
  void clear_product_model();
  static const int kProductModelFieldNumber = 3;
  ::logi::proto::Product_Model product_model() const;
  void set_product_model(::logi::proto::Product_Model value);

  // uint64 expiration_millis = 4;
  void clear_expiration_millis();
  static const int kExpirationMillisFieldNumber = 4;
  ::google::protobuf::uint64 expiration_millis() const;
  void set_expiration_millis(::google::protobuf::uint64 value);

  // uint32 reporting_interval_seconds = 5;
  void clear_reporting_interval_seconds();
  static const int kReportingIntervalSecondsFieldNumber = 5;
  ::google::protobuf::uint32 reporting_interval_seconds() const;
  void set_reporting_interval_seconds(::google::protobuf::uint32 value);

  // @@protoc_insertion_point(class_scope:logi.proto.LRCheckForProductUpdateRequest)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::internal::ArenaStringPtr product_uuid_;
  bool update_now_;
  int product_model_;
  ::google::protobuf::uint64 expiration_millis_;
  ::google::protobuf::uint32 reporting_interval_seconds_;
  mutable ::google::protobuf::internal::CachedSize _cached_size_;
  friend struct ::protobuf_cloud_5fdevice_5frequests_2eproto::TableStruct;
};
// -------------------------------------------------------------------

class LRCheckForProductUpdateResponse : public ::google::protobuf::Message /* @@protoc_insertion_point(class_definition:logi.proto.LRCheckForProductUpdateResponse) */ {
 public:
  LRCheckForProductUpdateResponse();
  virtual ~LRCheckForProductUpdateResponse();

  LRCheckForProductUpdateResponse(const LRCheckForProductUpdateResponse& from);

  inline LRCheckForProductUpdateResponse& operator=(const LRCheckForProductUpdateResponse& from) {
    CopyFrom(from);
    return *this;
  }
  #if LANG_CXX11
  LRCheckForProductUpdateResponse(LRCheckForProductUpdateResponse&& from) noexcept
    : LRCheckForProductUpdateResponse() {
    *this = ::std::move(from);
  }

  inline LRCheckForProductUpdateResponse& operator=(LRCheckForProductUpdateResponse&& from) noexcept {
    if (GetArenaNoVirtual() == from.GetArenaNoVirtual()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }
  #endif
  static const ::google::protobuf::Descriptor* descriptor();
  static const LRCheckForProductUpdateResponse& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const LRCheckForProductUpdateResponse* internal_default_instance() {
    return reinterpret_cast<const LRCheckForProductUpdateResponse*>(
               &_LRCheckForProductUpdateResponse_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  void Swap(LRCheckForProductUpdateResponse* other);
  friend void swap(LRCheckForProductUpdateResponse& a, LRCheckForProductUpdateResponse& b) {
    a.Swap(&b);
  }

  // implements Message ----------------------------------------------

  inline LRCheckForProductUpdateResponse* New() const final {
    return CreateMaybeMessage<LRCheckForProductUpdateResponse>(NULL);
  }

  LRCheckForProductUpdateResponse* New(::google::protobuf::Arena* arena) const final {
    return CreateMaybeMessage<LRCheckForProductUpdateResponse>(arena);
  }
  void CopyFrom(const ::google::protobuf::Message& from) final;
  void MergeFrom(const ::google::protobuf::Message& from) final;
  void CopyFrom(const LRCheckForProductUpdateResponse& from);
  void MergeFrom(const LRCheckForProductUpdateResponse& from);
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
  void InternalSwap(LRCheckForProductUpdateResponse* other);
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

  // repeated .logi.proto.Error errors = 1;
  int errors_size() const;
  void clear_errors();
  static const int kErrorsFieldNumber = 1;
  ::logi::proto::Error* mutable_errors(int index);
  ::google::protobuf::RepeatedPtrField< ::logi::proto::Error >*
      mutable_errors();
  const ::logi::proto::Error& errors(int index) const;
  ::logi::proto::Error* add_errors();
  const ::google::protobuf::RepeatedPtrField< ::logi::proto::Error >&
      errors() const;

  // bool success = 2;
  void clear_success();
  static const int kSuccessFieldNumber = 2;
  bool success() const;
  void set_success(bool value);

  // @@protoc_insertion_point(class_scope:logi.proto.LRCheckForProductUpdateResponse)
 private:

  ::google::protobuf::internal::InternalMetadataWithArena _internal_metadata_;
  ::google::protobuf::RepeatedPtrField< ::logi::proto::Error > errors_;
  bool success_;
  mutable ::google::protobuf::internal::CachedSize _cached_size_;
  friend struct ::protobuf_cloud_5fdevice_5frequests_2eproto::TableStruct;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// LRCheckForProductUpdateRequest

// bool update_now = 1;
inline void LRCheckForProductUpdateRequest::clear_update_now() {
  update_now_ = false;
}
inline bool LRCheckForProductUpdateRequest::update_now() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRCheckForProductUpdateRequest.update_now)
  return update_now_;
}
inline void LRCheckForProductUpdateRequest::set_update_now(bool value) {
  
  update_now_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.LRCheckForProductUpdateRequest.update_now)
}

// string product_uuid = 2;
inline void LRCheckForProductUpdateRequest::clear_product_uuid() {
  product_uuid_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline const ::std::string& LRCheckForProductUpdateRequest::product_uuid() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRCheckForProductUpdateRequest.product_uuid)
  return product_uuid_.GetNoArena();
}
inline void LRCheckForProductUpdateRequest::set_product_uuid(const ::std::string& value) {
  
  product_uuid_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:logi.proto.LRCheckForProductUpdateRequest.product_uuid)
}
#if LANG_CXX11
inline void LRCheckForProductUpdateRequest::set_product_uuid(::std::string&& value) {
  
  product_uuid_.SetNoArena(
    &::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::move(value));
  // @@protoc_insertion_point(field_set_rvalue:logi.proto.LRCheckForProductUpdateRequest.product_uuid)
}
#endif
inline void LRCheckForProductUpdateRequest::set_product_uuid(const char* value) {
  GOOGLE_DCHECK(value != NULL);
  
  product_uuid_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:logi.proto.LRCheckForProductUpdateRequest.product_uuid)
}
inline void LRCheckForProductUpdateRequest::set_product_uuid(const char* value, size_t size) {
  
  product_uuid_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:logi.proto.LRCheckForProductUpdateRequest.product_uuid)
}
inline ::std::string* LRCheckForProductUpdateRequest::mutable_product_uuid() {
  
  // @@protoc_insertion_point(field_mutable:logi.proto.LRCheckForProductUpdateRequest.product_uuid)
  return product_uuid_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* LRCheckForProductUpdateRequest::release_product_uuid() {
  // @@protoc_insertion_point(field_release:logi.proto.LRCheckForProductUpdateRequest.product_uuid)
  
  return product_uuid_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void LRCheckForProductUpdateRequest::set_allocated_product_uuid(::std::string* product_uuid) {
  if (product_uuid != NULL) {
    
  } else {
    
  }
  product_uuid_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), product_uuid);
  // @@protoc_insertion_point(field_set_allocated:logi.proto.LRCheckForProductUpdateRequest.product_uuid)
}

// .logi.proto.Product.Model product_model = 3;
inline void LRCheckForProductUpdateRequest::clear_product_model() {
  product_model_ = 0;
}
inline ::logi::proto::Product_Model LRCheckForProductUpdateRequest::product_model() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRCheckForProductUpdateRequest.product_model)
  return static_cast< ::logi::proto::Product_Model >(product_model_);
}
inline void LRCheckForProductUpdateRequest::set_product_model(::logi::proto::Product_Model value) {
  
  product_model_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.LRCheckForProductUpdateRequest.product_model)
}

// uint64 expiration_millis = 4;
inline void LRCheckForProductUpdateRequest::clear_expiration_millis() {
  expiration_millis_ = GOOGLE_ULONGLONG(0);
}
inline ::google::protobuf::uint64 LRCheckForProductUpdateRequest::expiration_millis() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRCheckForProductUpdateRequest.expiration_millis)
  return expiration_millis_;
}
inline void LRCheckForProductUpdateRequest::set_expiration_millis(::google::protobuf::uint64 value) {
  
  expiration_millis_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.LRCheckForProductUpdateRequest.expiration_millis)
}

// uint32 reporting_interval_seconds = 5;
inline void LRCheckForProductUpdateRequest::clear_reporting_interval_seconds() {
  reporting_interval_seconds_ = 0u;
}
inline ::google::protobuf::uint32 LRCheckForProductUpdateRequest::reporting_interval_seconds() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRCheckForProductUpdateRequest.reporting_interval_seconds)
  return reporting_interval_seconds_;
}
inline void LRCheckForProductUpdateRequest::set_reporting_interval_seconds(::google::protobuf::uint32 value) {
  
  reporting_interval_seconds_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.LRCheckForProductUpdateRequest.reporting_interval_seconds)
}

// -------------------------------------------------------------------

// LRCheckForProductUpdateResponse

// repeated .logi.proto.Error errors = 1;
inline int LRCheckForProductUpdateResponse::errors_size() const {
  return errors_.size();
}
inline ::logi::proto::Error* LRCheckForProductUpdateResponse::mutable_errors(int index) {
  // @@protoc_insertion_point(field_mutable:logi.proto.LRCheckForProductUpdateResponse.errors)
  return errors_.Mutable(index);
}
inline ::google::protobuf::RepeatedPtrField< ::logi::proto::Error >*
LRCheckForProductUpdateResponse::mutable_errors() {
  // @@protoc_insertion_point(field_mutable_list:logi.proto.LRCheckForProductUpdateResponse.errors)
  return &errors_;
}
inline const ::logi::proto::Error& LRCheckForProductUpdateResponse::errors(int index) const {
  // @@protoc_insertion_point(field_get:logi.proto.LRCheckForProductUpdateResponse.errors)
  return errors_.Get(index);
}
inline ::logi::proto::Error* LRCheckForProductUpdateResponse::add_errors() {
  // @@protoc_insertion_point(field_add:logi.proto.LRCheckForProductUpdateResponse.errors)
  return errors_.Add();
}
inline const ::google::protobuf::RepeatedPtrField< ::logi::proto::Error >&
LRCheckForProductUpdateResponse::errors() const {
  // @@protoc_insertion_point(field_list:logi.proto.LRCheckForProductUpdateResponse.errors)
  return errors_;
}

// bool success = 2;
inline void LRCheckForProductUpdateResponse::clear_success() {
  success_ = false;
}
inline bool LRCheckForProductUpdateResponse::success() const {
  // @@protoc_insertion_point(field_get:logi.proto.LRCheckForProductUpdateResponse.success)
  return success_;
}
inline void LRCheckForProductUpdateResponse::set_success(bool value) {
  
  success_ = value;
  // @@protoc_insertion_point(field_set:logi.proto.LRCheckForProductUpdateResponse.success)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace proto
}  // namespace logi

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_INCLUDED_cloud_5fdevice_5frequests_2eproto

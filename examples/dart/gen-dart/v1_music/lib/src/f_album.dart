// Autogenerated by Frugal Compiler (2.22.2)
// DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING

import 'dart:typed_data' show Uint8List;
import 'package:thrift/thrift.dart' as thrift;
import 'package:v1_music/v1_music.dart' as t_v1_music;

/// The IDL provides set, list, and map types for representing collections
/// of data.  Our Album struct contains a list of Tracks.
class Album implements thrift.TBase {
  static final thrift.TStruct _STRUCT_DESC = new thrift.TStruct("Album");
  static final thrift.TField _TRACKS_FIELD_DESC = new thrift.TField("tracks", thrift.TType.LIST, 1);
  static final thrift.TField _DURATION_FIELD_DESC = new thrift.TField("duration", thrift.TType.DOUBLE, 2);
  static final thrift.TField _ASIN_FIELD_DESC = new thrift.TField("ASIN", thrift.TType.STRING, 3);

  List<t_v1_music.Track> tracks;
  static const int TRACKS = 1;
  double duration = 0.0;
  static const int DURATION = 2;
  String aSIN;
  static const int ASIN = 3;


  Album() {
  }

  @deprecated
  bool isSetTracks() => tracks == null;

  @deprecated
  unsetTracks() => tracks = null;

  @deprecated
  bool isSetDuration() => duration == null;

  @deprecated
  unsetDuration() => duration = null;

  @deprecated
  bool isSetASIN() => ASIN == null;

  @deprecated
  unsetASIN() => ASIN = null;

  getFieldValue(int fieldID) {
    switch (fieldID) {
      case TRACKS:
        return this.tracks;
      case DURATION:
        return this.duration;
      case ASIN:
        return this.aSIN;
      default:
        throw new ArgumentError("Field $fieldID doesn't exist!");
    }
  }

  setFieldValue(int fieldID, Object value) {
    switch(fieldID) {
      case TRACKS:
        if (value == null) {
          tracks = null;
        } else if (value is List<t_v1_music.Track>) {
          tracks = value;
        }

        break;

      case DURATION:
        if (value == null) {
          duration = null;
        } else if (value is double) {
          duration = value;
        }

        break;

      case ASIN:
        if (value == null) {
          aSIN = null;
        } else if (value is String) {
          aSIN = value;
        }

        break;

      default:
        throw new ArgumentError("Field $fieldID doesn't exist!");
    }
  }

  // Returns true if the field corresponding to fieldID is set (has been assigned a value) and false otherwise
  bool isSet(int fieldID) {
    switch(fieldID) {
      case TRACKS:
        return tracks == null;

      case DURATION:
        return duration == null;

      case ASIN:
        return ASIN == null;

      default:
        throw new ArgumentError("Field $fieldID doesn't exist!");
    }
  }

  read(thrift.TProtocol iprot) {
    thrift.TField field;
    iprot.readStructBegin();
    while(true) {
      field = iprot.readFieldBegin();
      if(field.type == thrift.TType.STOP) {
        break;
      }
      switch(field.id) {
        case TRACKS:
          if(field.type == thrift.TType.LIST) {
            thrift.TList elem0 = iprot.readListBegin();
            tracks = new List<t_v1_music.Track>();
            for(int elem2 = 0; elem2 < elem0.length; ++elem2) {
              t_v1_music.Track elem1 = new t_v1_music.Track();
              elem1.read(iprot);
              tracks.add(elem1);
            }
            iprot.readListEnd();
          } else {
            thrift.TProtocolUtil.skip(iprot, field.type);
          }
          break;
        case DURATION:
          if(field.type == thrift.TType.DOUBLE) {
            duration = iprot.readDouble();
          } else {
            thrift.TProtocolUtil.skip(iprot, field.type);
          }
          break;
        case ASIN:
          if(field.type == thrift.TType.STRING) {
            aSIN = iprot.readString();
          } else {
            thrift.TProtocolUtil.skip(iprot, field.type);
          }
          break;
        default:
          thrift.TProtocolUtil.skip(iprot, field.type);
          break;
      }
      iprot.readFieldEnd();
    }
    iprot.readStructEnd();

    validate();
  }

  write(thrift.TProtocol oprot) {
    validate();

    oprot.writeStructBegin(_STRUCT_DESC);
    if(this.tracks != null) {
      oprot.writeFieldBegin(_TRACKS_FIELD_DESC);
      oprot.writeListBegin(new thrift.TList(thrift.TType.STRUCT, tracks.length));
      for(var elem3 in tracks) {
        elem3.write(oprot);
      }
      oprot.writeListEnd();
      oprot.writeFieldEnd();
    }
    oprot.writeFieldBegin(_DURATION_FIELD_DESC);
    oprot.writeDouble(duration);
    oprot.writeFieldEnd();
    if(this.aSIN != null) {
      oprot.writeFieldBegin(_ASIN_FIELD_DESC);
      oprot.writeString(aSIN);
      oprot.writeFieldEnd();
    }
    oprot.writeFieldStop();
    oprot.writeStructEnd();
  }

  String toString() {
    StringBuffer ret = new StringBuffer("Album(");

    ret.write("tracks:");
    if(this.tracks == null) {
      ret.write("null");
    } else {
      ret.write(this.tracks);
    }

    ret.write(", ");
    ret.write("duration:");
    ret.write(this.duration);

    ret.write(", ");
    ret.write("aSIN:");
    if(this.aSIN == null) {
      ret.write("null");
    } else {
      ret.write(this.aSIN);
    }

    ret.write(")");

    return ret.toString();
  }

  bool operator ==(Object o) {
    if(o == null || !(o is Album)) {
      return false;
    }
    Album other = o as Album;
    return this.tracks == other.tracks
      && this.duration == other.duration
      && this.aSIN == other.aSIN;
  }

  int get hashCode {
    var value = 17;
    value = (value * 31) ^ tracks.hashCode;
    value = (value * 31) ^ duration.hashCode;
    value = (value * 31) ^ aSIN.hashCode;
    return value;
  }

  Album clone({
    List<t_v1_music.Track> tracks: null,
    double duration: null,
    String aSIN: null,
  }) {
    return new Album()
      ..tracks = tracks ?? this.tracks
      ..duration = duration ?? this.duration
      ..aSIN = aSIN ?? this.aSIN;
  }

  validate() {
  }
}


class _constant:
    class ConstError(TypeError):pass
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Cannot rebind const (%s)" %name)
        self.__dict__[name] = value


# SOARINGALANO_CONST = _constant()
#
# SOARINGALANO_CONST.EXCHANGE_NAME = "soaringalano_cloud_msgq"
# SOARINGALANO_CONST.QUEUE_STDOUT = "stdout"
# SOARINGALANO_CONST.QUEUE_STDERR = "stderr"


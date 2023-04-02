import uuid

from rest_framework import serializers

from alias.models import Alias


class AliasCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = ('target', 'alias')
        read_only_fields = ('alias', )

    def create(self, validated_data):
        if obj := Alias.objects.filter(target=validated_data['target']).first():
            return obj

        qs = Alias.objects.all()
        existing_aliases = set(qs.values_list('alias', flat=True))
        while (alias := self._generate_alias()) in existing_aliases:
            continue

        return super().create({**validated_data, 'alias': alias})

    @staticmethod
    def _generate_alias(length: int = 6) -> str:
        return uuid.uuid4().hex.upper()[:length]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['alias'] = f'http://localhost:8000/{ret["alias"]}'

        return ret


class AliasDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alias
        fields = ('target', )
        read_only_fields = fields

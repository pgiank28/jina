import os

import pytest
import numpy as np

from jina.executors import BaseExecutor

@pytest.mark.parametrize('replica_id', [1,2,3])
def test_share_workspace(tmpdir, replica_id):
    with BaseExecutor.load_config('yaml/test-workspace.yml', True, replica_id) as executor:
        executor.touch()
        executor_dir = tmpdir.join(f'{executor.name}-{replica_id}-{executor.name}.bin')
        executor.save(executor_dir)
        assert os.path.exists(executor_dir)

@pytest.mark.parametrize('replica_id', [1,2,3])
def test_compound_workspace(tmpdir, replica_id):
    with BaseExecutor.load_config('yaml/test-compound-workspace.yml', True, replica_id) as executor:
        for c in executor.components:
            c.touch()
            component_dir = tmpdir.join(f'{executor.name}-{replica_id}-{c.name}.bin')
            c.save(component_dir)
            assert os.path.exists(component_dir)
        executor.touch()
        executor_dir = tmpdir.join(f'{executor.name}-{replica_id}-{executor.name}.bin')
        assert os.path.exists(executor_dir)

@pytest.mark.parametrize('replica_id', [1,2,3])
def test_compound_indexer(tmpdir, replica_id):
    with BaseExecutor.load_config('yaml/test-compound-indexer.yml', True, replica_id) as e:
        for c in e:
            c.touch()
            component_dir = tmpdir.join(f'{e.name}-{replica_id}-{c.name}.bin')
            c.save(component_dir)
            assert os.path.exists(c.index_abspath)
            assert c.save_abspath.startswith(e.current_workspace)
            assert c.index_abspath.startswith(e.current_workspace)

        e.touch()
        executor_dir = tmpdir.join(f'{e.name}-{replica_id}-{e.name}.bin')
        e.save(executor_dir)
        assert os.path.exists(e.save_abspath)

def test_compound_indexer_rw():
    pass
    # TODO: need refactor.
    # all_vecs = np.random.random([6, 5])
    # for j in range(3):
    #     a = BaseExecutor.load_config('yaml/test-compound-indexer2.yml', True, j)
    #     assert a[0] == a['test_meta']
    #     assert not a[0].is_updated
    #     assert not a.is_updated
    #     a[0].add([j, j * 2, j * 3], [bytes(j), bytes(j * 2), bytes(j * 3)])
    #     assert a[0].is_updated
    #     assert a.is_updated
    #     assert not a[1].is_updated
    #     a[1].add(np.array([j * 2, j * 2 + 1]), all_vecs[(j * 2, j * 2 + 1), :])
    #     assert a[1].is_updated
    #     a.save()
    #     # the compound executor itself is not modified, therefore should not generate a save
    #     assert not os.path.exists(a.save_abspath)
    #     assert os.path.exists(a[0].save_abspath)
    #     assert os.path.exists(a[0].index_abspath)
    #     assert os.path.exists(a[1].save_abspath)
    #     assert os.path.exists(a[1].index_abspath)
    #
    # recovered_vecs = []
    # for j in range(3):
    #     a = BaseExecutor.load_config('yaml/test-compound-indexer2.yml', True, j)
    #     recovered_vecs.append(a[1].query_handler)
    #
    # np.testing.assert_almost_equal(all_vecs, np.concatenate(recovered_vecs))
